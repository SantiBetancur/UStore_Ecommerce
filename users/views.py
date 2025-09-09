from django.shortcuts import render
from django.views import View 

class LoginView(View):
    template_name = 'pages/login.html'
    def get(self, request):
        context = {
            'title': 'Ingresar'
        }
        return render(request, self.template_name, context)

class SingInView(View):
    template_name = 'pages/signIn.html'
    def get(self, request):
        context = {
            'title': 'Regístrate'
        }
        return render(request, self.template_name, context)