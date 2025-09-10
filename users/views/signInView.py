from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.views import View 
from ..models import User

data_get_render_template = {
            'title': 'Registro',
            "p_text": "¿Ya estas registrado?",
            "a_text": "inicia sección aquí",
            "btn_text": "Registrarse",
            "url_redirect": "login",
            'select': {
                'name': 'role',
                'options': [
                    {'value': False, 'text': 'Comprador'},
                    {'value': True, 'text': 'Vendedor'},
                ]
            },
            'form_fields': [
                {
                    "id":"name",
                    'type': 'text',
                    'label': 'Nombre',
                    'placeholder': 'Ingrese su nombre'
                },{
                    "id":"email",
                    'type': 'email',
                    'label': 'Email',
                    'placeholder': 'Ingrese su email'
                },{
                    "id":"cellphone",
                    'type': 'text',
                    'label': 'Celular',
                    'placeholder': 'Ingrese su celular'
                },{
                    "id":"password",
                    'type': 'password',
                    'label': 'Contraseña',
                    'placeholder': 'ingrese su contraseña'
                }
            ]
        }

class SingInView(View):
    template_name = 'pages/forms.html'

    def get(self, request):
        data_get_render_template.pop("errors", None)
        return render(request, self.template_name, data_get_render_template)

    def post(self, request):
        data_get_render_template.pop("errors", None)

        email = request.POST.get("email")
        name = request.POST.get("name")
        cellphone = request.POST.get("cellphone")
        role = request.POST.get("role")
        password = request.POST.get("password")

        try:
            validate_password(password)
        except ValidationError as e:
            data_get_render_template["errors"] = e.messages
        try:
            if not data_get_render_template.get("errors"):        
                newUser = User.objects.create_user(
                    email=email,
                    name=name,
                    password=password,
                    cellphone=cellphone,
                    has_store=role,
                )

                return redirect("landing") 
        except Exception as e:
            print(e)
            data_get_render_template["errors"] = ["El correo ya está en uso."]

        return render(request, self.template_name, data_get_render_template)