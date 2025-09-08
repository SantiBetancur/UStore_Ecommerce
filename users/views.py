from django.shortcuts import render
from django.views import View 

class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        data = {
            'title': 'Login'
        }
        return render(request, self.template_name, data)

class SingInView(View):
    template_name = 'signin.html'
    def get(self, request):
        data = {
            'title': 'Sing in'
        }
        return render(request, self.template_name, data)