from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.shortcuts import redirect


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_user(self, request, sociallogin, data):
        """Poblar el usuario con datos del proveedor social."""
        user = super().populate_user(request, sociallogin, data)
        full_name = data.get("name") or (f"{data.get('given_name', '').strip()} {data.get('family_name', '').strip()}".strip())
        if full_name:
            user.name = full_name
        return user
    
    def pre_social_login(self, request, sociallogin):
        """Se ejecuta antes de hacer login social.
        Si el email ya existe, vincula la cuenta social y hace login automáticamente."""
        User = get_user_model()
        
        # Obtener el email del sociallogin
        # El email puede estar en account.extra_data o en el usuario temporal
        email = None
        if hasattr(sociallogin, 'account') and sociallogin.account:
            # Intentar obtener el email de extra_data
            email = sociallogin.account.extra_data.get('email')
            if not email and hasattr(sociallogin.account, 'extra_data'):
                # Algunos proveedores usan diferentes claves
                email = sociallogin.account.extra_data.get('emailAddress') or \
                       sociallogin.account.extra_data.get('email_address')
        
        # Si aún no tenemos email, intentar del usuario temporal
        if not email and hasattr(sociallogin, 'user') and sociallogin.user:
            email = getattr(sociallogin.user, 'email', None)
        
        if email:
            try:
                user = User.objects.get(email=email)
                sociallogin.user = user
            except User.DoesNotExist:
                extra = sociallogin.account.extra_data
                name = extra.get('name') or f"{extra.get('given_name', '')} {extra.get('family_name', '')}".strip()

                request.session['social_signup_data'] = {
                    'email': email,
                    'name': name
                }

                raise ImmediateHttpResponse(redirect('signin'))

