from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.db import models
from market_pages.models import Store  


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)

        validate_password(password)

        user = self.model(
            email=email,
            name=name,
            **extra_fields
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    cellphone = models.CharField(max_length=15, blank=True, null=True)
    has_store = models.BooleanField(default=False)
    store = models.ForeignKey("market_pages.Store", on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def create_store(self, name, description, logo):
        if self.has_store:
            raise ValueError("User already has a store.")
        
        store = Store.objects.create(
            name=name,
            description=description,
            logo=logo if logo else None,
        )
        self.store = store
        self.has_store = True
        self.save()
        return store

    def __str__(self):
        return self.email
