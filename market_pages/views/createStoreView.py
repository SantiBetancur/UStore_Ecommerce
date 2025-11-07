from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse

import logging
logger = logging.getLogger(__name__)
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def guardar_logo_en_static(logo_file):
    """Guarda el logo en la carpeta static/store_logos/ y retorna la ruta relativa"""
    static_path = os.path.join(settings.BASE_DIR, "market_pages", 'static', 'store_logos')
    os.makedirs(static_path, exist_ok=True)

    fs = FileSystemStorage(location=static_path)
    filename = fs.save(logo_file.name, logo_file)
    file_url = os.path.join('store_logos', filename)
    
    print(f"✅ Logo guardado en: {file_url}")
    return file_url

class CreateStore(LoginRequiredMixin, TemplateView):
    template_name = 'pages/createStore.html'
    login_url = 'login'   

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        error_message = request.GET.get('error')
        
        username = request.session.get('username', '')
        storename = request.session.get('short_storename', '') if request.session.get('short_storename', '') else "Mi tienda"
        cart_count = request.session.get('cart_count', 0)
        context = {
            'page_title': 'Tienda',
            'username': username,
            'storename': storename,
            'cart_count': cart_count,
            'error': error_message,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("store_name")
        description = request.POST.get("description")
        logo = request.FILES.get("logo")

        print("=== DEPURACIÓN DE LOGO ===")
        print("FILES:", request.FILES)
        if logo:
            print(f"Logo recibido: {logo.name}")
            logo_path = guardar_logo_en_static(logo)  # 👈 Guardar en static
        else:
            print("⚠️ No se recibió ningún logo")
            logo_path = None

        store = request.user.create_store(name, description, logo_path)

        try:
            if store.get("error", None):
                return redirect(f"{reverse('create_store')}?error={store.get('error')}")
        except:
            pass

        short_storename = name[:20] + '...' if len(name) > 20 else name
        request.session['store'] = name
        request.session['short_storename'] = short_storename

        print(f"Tienda creada: {name} por {request.user.email}")
        print(f"Logo guardado en: {logo_path}")

        return redirect('landing')
