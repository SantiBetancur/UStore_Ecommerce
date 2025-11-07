from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages

from market_pages.models import Product  # Verifica que esta ruta sea correcta
from market_pages.forms import ProductForm  # Formulario para crear productos

import logging
logger = logging.getLogger(__name__)


class AdminStore(LoginRequiredMixin, TemplateView):
    template_name = 'pages/adminStore.html'
    login_url = 'login'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        username = request.session.get('username', '')
        storename = request.session.get('short_storename', '') if request.session.get('short_storename', '') else "Mi tienda"
        cart_count = request.session.get('cart_count', 0)

        # 🔹 Obtener productos asociados a la tienda del usuario (si la tiene)
        if hasattr(request.user, 'store'):
            products = Product.objects.filter(store_id=request.user.store)
        else:
            products = []

        context = {
            'page_title': 'Tienda',
            'username': username,
            'storename': storename,
            'name': request.user.store.name if hasattr(request.user, 'store') else '',
            'description': request.user.store.description if hasattr(request.user, 'store') else '',
            'logo': request.user.store.logo if hasattr(request.user, 'store') else None,
            'cart_count': cart_count,
            'products': products,
            'product_count': len(products),
            'form': ProductForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Permite crear un nuevo producto desde el formulario."""
        if not request.user.is_authenticated:
            return redirect("login")

        if not hasattr(request.user, 'store'):
            messages.error(request, "No tienes una tienda asociada para agregar productos.")
            return redirect('admin-store')

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store_id = request.user.store  # 🔹 Se asigna la tienda, no el usuario
            product.save()
            messages.success(request, "Producto creado exitosamente.")
            logger.info(f"Nuevo producto creado: {product.name}")
        else:
            messages.error(request, "Ocurrió un error al crear el producto. Verifica los campos.")

        return redirect('admin-store')
