from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from market_pages.forms import ProductForm
from market_pages.models.ProductModel import Product


class CreateProductView(LoginRequiredMixin, View):
    template_name = 'pages/create_product.html'
    login_url = 'login'

    def get(self, request):
        # Verificar si el usuario tiene una tienda
        if not hasattr(request.user, 'store'):
            messages.error(request, "Debes tener una tienda para agregar productos.")
            return redirect('landing')

        form = ProductForm()
        return render(request, self.template_name, {
            'form': form,
            'title': 'Crear Producto'
        })

    def post(self, request):
        if not hasattr(request.user, 'store'):
            messages.error(request, "Debes tener una tienda para agregar productos.")
            return redirect('landing')

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store_id = request.user.store  # Asociar producto a la tienda
            product.save()
            messages.success(request, "Producto creado exitosamente.")
            return redirect('admin_store')  # Redirigir a la vista del panel de tienda
        else:
            messages.error(request, "Ocurrió un error al crear el producto. Verifica los campos.")

        return render(request, self.template_name, {
            'form': form,
            'title': 'Crear Producto'
        })
