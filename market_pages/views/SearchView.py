from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from ..models import Product

@require_http_methods(["GET"])
def search_products(request):
    """
    Vista para buscar productos en tiempo real
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:  # Mínimo 2 caracteres para buscar
        return JsonResponse({'products': []})
    
    # Buscar productos que coincidan con name, category o type usando Q objects
    products = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(category__icontains=query) | 
        Q(type__icontains=query)
    ).distinct()[:10]  # Limitar a 10 resultados
    
    # Convertir a formato JSON
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'type': product.type,
            'price': float(product.price),
            'image_url': product.image.url if product.image else '/static/images/default.png',
            'url': f'/product/{product.id}/'  # URL para ver el producto
        })
    
    return JsonResponse({'products': products_data})
