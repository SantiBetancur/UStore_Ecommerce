from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .UrbanLoomApi import get_urbanloom_client, UrbanLoomAPIClient
import logging

logger = logging.getLogger(__name__)


class UrbanLoomProductsView(View):
    """
    Vista para mostrar productos patrocinados de UrbanLoom.
    """
    template_name = 'pages/urbanloom_products.html'
    
    def get(self, request):
        """
        Obtiene y muestra los productos patrocinados de UrbanLoom.
        """
        # Obtener cliente de UrbanLoom
        client = get_urbanloom_client()
        
        # Intentar obtener productos
        urbanloom_response = client.get_products()
        
        # Variables del contexto
        products = []
        error_message = None
        success = False
        
        if urbanloom_response and urbanloom_response.get('success', False):
            # Obtener productos activos y normalizarlos
            raw_products = urbanloom_response.get('products', [])
            products = [
                UrbanLoomAPIClient.normalize_product(p) 
                for p in raw_products 
                if p.get('is_active', False)
            ]
            success = True
            count = len(products)
        else:
            error_message = "No se pudieron cargar los productos patrocinados de UrbanLoom. Por favor, intente más tarde."
            count = 0
        
        # Información del usuario para el contexto
        username = ''
        if request.user.is_authenticated:
            username = (request.user.name[:20] + '...') if hasattr(request.user, 'name') and len(request.user.name) > 20 else getattr(request.user, 'name', '')
        
        cart_count = request.session.get('cart_count', 0)
        
        context = {
            'products': products,
            'count': count,
            'success': success,
            'error_message': error_message,
            'page_title': 'Productos Patrocinados - UrbanLoom',
            'username': username,
            'user': request.user,
            'cart_count': cart_count,
        }
        
        return render(request, self.template_name, context)

