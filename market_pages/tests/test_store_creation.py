from django.test import TestCase
from django.contrib.auth import get_user_model
from market_pages.models import Store

User = get_user_model()

class StoreCreationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            name='Test User',
            password='TestPass123'
        )

    def test_create_store_success(self):
        store = Store.objects.create(name="Tienda Test", description="Descripción test")
        self.assertEqual(Store.objects.count(), 1)
        self.assertEqual(store.name, "Tienda Test")
