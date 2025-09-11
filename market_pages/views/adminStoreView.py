from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect

import logging
logger = logging.getLogger(__name__)
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
