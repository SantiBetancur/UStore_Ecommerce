from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

import logging
logger = logging.getLogger(__name__)
#todo: crear excepciones y mensajes para cuando una tienda tenga un nombre repetido y este tipo de cosas
class CreateStore(LoginRequiredMixin, TemplateView):
    template_name = 'pages/createStore.html'
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
            'cart_count': cart_count,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("store_name")
        description = request.POST.get("description")
        logo = request.FILES.get("logo") 
        logo=logo if logo else None
        request.user.create_store(name, description, logo)
        short_storename = name[:20] + '...' if len(name) > 20 else name
        request.session['store'] = name
        request.session['short_storename'] = short_storename

        print(f"Tienda creada: {name} por {request.user.email}")

        return redirect('landing')
