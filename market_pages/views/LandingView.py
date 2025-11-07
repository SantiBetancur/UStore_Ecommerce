from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import logging
from django.views.generic import TemplateView
from django.core.paginator import Paginator  # ✅ Import para la paginación
from ..models import Product, Cart, Favorite


logger = logging.getLogger(__name__)

class LandingView(TemplateView):
    template_name = 'pages/landing.html'

    def dispatch(self, request, *args, **kwargs):
        # Guardar nombre del usuario en la sesión solo si está autenticado
        if request.user.is_authenticated:
            username = (request.user.name[:20] + '...') if hasattr(request.user, 'name') and len(request.user.name) > 20 else getattr(request.user, 'name', '')
            request.session['username'] = username
        else:
            request.session['username'] = ''
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        # Obtener datos del usuario y la tienda
        username = request.session.get('username', '') if request.user.is_authenticated else ''
        storename = request.session.get('short_storename', '') if request.session.get('short_storename', '') else "Mi tienda"
        cart_count = request.session.get('cart_count', 0)
        
        # Obtener favoritos solo si el usuario está autenticado
        favorite_product_ids = []
        if request.user.is_authenticated:
            favorite_product_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)

        # --- Paginación de productos ---
        all_products = Product.objects.all().order_by('-created_at')  # productos más recientes primero
        paginator = Paginator(all_products, 12)  # 12 productos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # --- Contexto para el template ---
        context = {
            'products': page_obj,  # productos paginados
            'cart': Cart.objects.get_or_create(buyer=request.user)[0] if request.user.is_authenticated else None,
            'default_image': 'static/images/default.png',
            'page_title': 'UStore - Marketplace',
            'username': username,
            'user': request.user,
            'storename': storename,
            'cart_count': cart_count,
            'favorite_product_ids': favorite_product_ids,
        }

        return render(request, self.template_name, context)
