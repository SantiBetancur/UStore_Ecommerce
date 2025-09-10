from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View 
from ..models import User

data_get_render_template= {
            'title': 'Iniciar sesión',
            "p_text": "¿Aun no te has registrado?",
            "a_text": "Regístrate aquí",
            "btn_text": "Ingresar",
            "url_redirect": "signin",
            'form_fields': [
                {
                    "id":"user_email",
                    'type': 'email',
                    'label': 'Email',
                    'placeholder': 'Ingrese su email'
                },{
                    "id":"user_password",
                    'type': 'password',
                    'label': 'Contraseña',
                    'placeholder': 'ingrese su contraseña'
                }
            ]
        }

class LoginView(View):
    template_name = 'pages/forms.html'

    def get(self, request):
        data_get_render_template.pop("errors", None)
        return render(request, self.template_name, data_get_render_template)
    
    def post(self, request):
        data_get_render_template.pop("errors", None)

        email = request.POST.get("user_email")
        password = request.POST.get("user_password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("landing")  
        else:
            data_get_render_template["errors"] = ["Correo o contraseña incorrectos."]
            return render(request, self.template_name, data_get_render_template)
