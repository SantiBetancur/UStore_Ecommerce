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
        context = {
            'page_title': 'Tienda',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get("store_name")
        description = request.POST.get("description")
        logo = request.FILES.get("logo") 
        logo=logo if logo else None
        request.user.create_store(name, description, logo)

        print(f"Tienda creada: {name} por {request.user.email}")

        return redirect('landing')
