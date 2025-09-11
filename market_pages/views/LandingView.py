from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import logging
from django.views.generic import TemplateView
from ..models import Product

# Create your views here.

logger = logging.getLogger(__name__)



class LandingView(TemplateView):
    template_name = 'pages/landing.html'
    def get(self, request):
        # Shorten the username to 20 characters if it's longer
        username = (request.user.name[:20] + '...') if hasattr(request.user, 'name') and len(request.user.name) > 20 else getattr(request.user, 'name', '')
        context = {
            'products': Product.objects.all(),
            'default_image': 'static/images/default.png',
            'page_title': 'UStore - Marketplace',
            'username': username,
            'user': request.user
        }
        return render(request, self.template_name, context)