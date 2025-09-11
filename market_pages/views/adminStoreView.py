from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render

import logging
logger = logging.getLogger(__name__)
# Todo: actualizar datos de la tienda, es decir poder hacer ediciones
class AdminStore(LoginRequiredMixin, TemplateView):
    template_name = 'pages/adminStore.html'
    login_url = 'login'   

    def get(self, request, *args, **kwargs):
        context = {
            'page_title': 'Tienda',
            'name': request.user.store.name if request.user.has_store else '',
            'description': request.user.store.description if request.user.has_store else '',
            'logo': request.user.store.logo if request.user.has_store else None,
        }
        return render(request, self.template_name, context)
