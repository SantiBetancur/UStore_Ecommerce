from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

import logging
logger = logging.getLogger(__name__)
# import helper to save logo files
from .createStoreView import guardar_logo_en_static
# Todo: actualizar datos de la tienda, es decir poder hacer ediciones
class AdminStore(LoginRequiredMixin, TemplateView):
    template_name = 'pages/adminStore.html'
    login_url = 'login'   

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        username = request.session.get('username', '')
        storename = request.session.get('short_storename', '') if request.session.get('short_storename', '') else "Mi tienda"
        cart_count = request.session.get('cart_count', 0)

        context = {
            'page_title': 'Tienda',
            'username': username,
            'storename': storename,
            'name': request.user.store.name if request.user.has_store else '',
            'description': request.user.store.description if request.user.has_store else '',
            'logo': request.user.store.logo if request.user.has_store else None,
            'cart_count': cart_count,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """Maneja actualizaciones de la tienda (nombre, descripción y logo).
        Si llega un archivo 'logo' lo guarda en static/store_logos/ y actualiza el campo logo
        del modelo Store con la ruta relativa retornada por guardar_logo_en_static.
        """
        if not request.user.is_authenticated:
            return redirect("login")

        # Depuración: mostrar que se recibió una petición POST y qué archivos llegaron
        print("--- AdminStore POST ---")
        print("Method:", request.method)
        print("POST keys:", list(request.POST.keys()))
        print("FILES keys:", list(request.FILES.keys()))

        name = request.POST.get('name') or request.POST.get('store_name')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')

        if logo:
            try:
                print(f"Logo recibido en AdminStore: name={logo.name}, size={getattr(logo, 'size', 'unknown')}")
            except Exception as e:
                print("Error al obtener info de logo:", e)

        # solo continuar si el usuario tiene tienda creada
        if not request.user.has_store or not request.user.store:
            return redirect('create_store')

        store = request.user.store

        if name:
            store.name = name
        if description:
            store.description = description

        if logo:
            # guardar el logo en la misma carpeta que CreateStore
            logo_path = guardar_logo_en_static(logo)
            store.logo = logo_path

        store.save()

        return redirect('admin_store')
