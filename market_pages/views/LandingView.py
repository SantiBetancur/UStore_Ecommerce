from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import logging
from django.views.generic import TemplateView
from ..models import Product, Cart

# Create your views here.

logger = logging.getLogger(__name__)



class LandingView(TemplateView):
    template_name = 'pages/landing.html'
    def dispatch(self, request, *args, **kwargs):
        # Store the username in the session
        username = (request.user.name[:20] + '...') if hasattr(request.user, 'name') and len(request.user.name) > 20 else getattr(request.user, 'name', '')
        request.session['username'] = username
        return super().dispatch(request, *args, **kwargs)
    def get(self, request):
        # Shorten the username to 20 characters if it's longer
        username = request.session.get('username', '') if request.user.is_authenticated else ''
        context = {
            'products': Product.objects.all(),
            'cart': Cart.objects.get(buyer=request.user) if request.user.is_authenticated else None,
            'default_image': 'static/images/default.png',
            'page_title': 'UStore - Marketplace',
            'username': username,
            'user': request.user
        }
        return render(request, self.template_name, context)