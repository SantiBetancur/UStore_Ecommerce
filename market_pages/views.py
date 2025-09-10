from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import logging
from django.views.generic import TemplateView

# Create your views here.

logger = logging.getLogger(__name__)

class Product:
    def __init__(self, name, category, description, price, image):
        self.name = name
        self.category = category
        self.description = description
        self.price = price
        self.image = image

# 10 generic products

products = [
    Product('Product 1', 'Producto', 'Description 1', 100, 'static/images/Default Card Photo.png'),
    Product('Product 2', 'Servicio', 'Description 2', 200, 'static/images/Default Card Photo.png'),
    Product('Product 3', 'Producto','Description 3', 300, 'static/images/Default Card Photo.png'),
    Product('Product 4', 'Producto', 'Description 4', 400, 'static/images/Default Card Photo.png'),
    Product('Product 5', 'Servicio', 'Description 5', 500, 'static/images/Default Card Photo.png'),
    Product('Product 6', 'Producto', 'Description 6', 600, 'static/images/Default Card Photo.png'),
    Product('Product 7', 'Servicio', 'Description 7', 700, 'static/images/Default Card Photo.png'),
    Product('Product 8', 'Producto', 'Description 8', 800, 'static/images/Default Card Photo.png'),
    Product('Product 9', 'Servicio', 'Description 9', 900, 'static/images/Default Card Photo.png'),
    Product('Product 10', 'Producto', 'Description 10', 1000, 'static/images/Default Card Photo.png'),
]

class LandingView(TemplateView):
    template_name = 'pages/landing.html'
    def get(self, request):
        
        context = {
            'products': products,
            'page_title': 'UStore - Marketplace',
        }
        return render(request, self.template_name, context)

