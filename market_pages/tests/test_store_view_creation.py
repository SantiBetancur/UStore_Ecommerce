from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from market_pages.models import Store

User = get_user_model()

class CreateStoreViewTest(TestCase):
    def setUp(self):
        # Crear usuario de prueba y autenticarlo
        self.user = User.objects.create_user(
            email='testuser@example.com',
            name='Test User',
            password='testpassword'
        )
        self.client = Client()
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_create_store_successfully(self):
        """Verifica que se pueda crear una tienda usando la vista"""
        response = self.client.post('/create-store/', {
            'store_name': 'Mi Tienda Desde Vista',
            'description': 'Tienda creada desde la vista de prueba'
        })

        # La tienda debe haberse creado
        self.assertTrue(Store.objects.filter(name='Mi Tienda Desde Vista').exists())

        # El status code debe ser una redirección (por ejemplo, 302)
        self.assertEqual(response.status_code, 302)

    def test_create_store_view_redirects_if_not_logged_in(self):
        """Verifica que se redirija al login si no está autenticado"""
        client = Client()
        response = client.get('/create-store/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.url)
