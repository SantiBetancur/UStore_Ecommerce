from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from ..models import Product, Store
from rest_framework.views import APIView


@require_http_methods(["GET"])

class ProductAPIView(APIView):
    def products_api(request):
        """
        API REST para obtener productos disponibles con todos sus atributos.
        
        Parámetros de consulta opcionales:
        - category: Filtrar por categoría
        - type: Filtrar por tipo (product/service)
        - store_id: Filtrar por ID de tienda
        - min_price: Precio mínimo
        - max_price: Precio máximo
        - search: Buscar por nombre, categoría o tipo
        - limit: Limitar número de resultados (default: 100)
        - offset: Offset para paginación (default: 0)
        """
        try:
            # Obtener parámetros de consulta
            category = request.GET.get('category', '').strip()
            product_type = request.GET.get('type', '').strip()
            store_id = request.GET.get('store_id', '').strip()
            min_price = request.GET.get('min_price', '').strip()
            max_price = request.GET.get('max_price', '').strip()
            search = request.GET.get('search', '').strip()
            limit = int(request.GET.get('limit', 100))
            offset = int(request.GET.get('offset', 0))
            
            # Validar límite
            if limit > 1000:
                limit = 1000
            if limit < 1:
                limit = 100
            
            # Validar offset
            if offset < 0:
                offset = 0
            
            # Construir query
            queryset = Product.objects.all()
            
            # Aplicar filtros
            if category:
                queryset = queryset.filter(category__icontains=category)
            
            if product_type:
                queryset = queryset.filter(type__icontains=product_type)
            
            if store_id:
                try:
                    queryset = queryset.filter(store_id__market_id=int(store_id))
                except (ValueError, TypeError):
                    return JsonResponse({
                        'error': 'store_id debe ser un número válido'
                    }, status=400)
            
            if min_price:
                try:
                    queryset = queryset.filter(price__gte=float(min_price))
                except (ValueError, TypeError):
                    return JsonResponse({
                        'error': 'min_price debe ser un número válido'
                    }, status=400)
            
            if max_price:
                try:
                    queryset = queryset.filter(price__lte=float(max_price))
                except (ValueError, TypeError):
                    return JsonResponse({
                        'error': 'max_price debe ser un número válido'
                    }, status=400)
            
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(category__icontains=search) |
                    Q(type__icontains=search) |
                    Q(description__icontains=search)
                )
            
            # Obtener total antes de aplicar paginación
            total_count = queryset.count()
            
            # Aplicar paginación
            queryset = queryset.order_by('-created_at')[offset:offset + limit]
            
            # Construir respuesta
            products_data = []
            for product in queryset:
                # Obtener URL de la imagen
                image_url = None
                if product.image:
                    if request.is_secure():
                        protocol = 'https'
                    else:
                        protocol = 'http'
                    host = request.get_host()
                    image_url = f"{protocol}://{host}{product.image.url}"
                
                # Información de la tienda
                store_info = None
                if product.store_id:
                    store_info = {
                        'id': product.store_id.market_id,
                        'name': product.store_id.name,
                        'description': product.store_id.description,
                        'logo': product.store_id.logo
                    }
                
                products_data.append({
                    'id': product.id,
                    'name': product.name,
                    'category': product.category,
                    'type': product.type,
                    'description': product.description,
                    'price': float(product.price),
                    'image_url': image_url,
                    'created_at': product.created_at.isoformat(),
                    'updated_at': product.updated_at.isoformat(),
                    'store': store_info
                })
            
            # Respuesta JSON
            response_data = {
                'success': True,
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'count': len(products_data),
                'products': products_data
            }
            
            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False})
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


    @require_http_methods(["GET"])
    def product_detail_api(request, product_id):
        """
        API REST para obtener un producto específico por su ID.
        """
        try:
            product = Product.objects.get(id=product_id)
            
            # Obtener URL de la imagen
            image_url = None
            if product.image:
                if request.is_secure():
                    protocol = 'https'
                else:
                    protocol = 'http'
                host = request.get_host()
                image_url = f"{protocol}://{host}{product.image.url}"
            
            # Información de la tienda
            store_info = None
            if product.store_id:
                store_info = {
                    'id': product.store_id.market_id,
                    'name': product.store_id.name,
                    'description': product.store_id.description,
                    'logo': product.store_id.logo
                }
            
            product_data = {
                'id': product.id,
                'name': product.name,
                'category': product.category,
                'type': product.type,
                'description': product.description,
                'price': float(product.price),
                'image_url': image_url,
                'created_at': product.created_at.isoformat(),
                'updated_at': product.updated_at.isoformat(),
                'store': store_info
            }
            
            return JsonResponse({
                'success': True,
                'product': product_data
            }, json_dumps_params={'ensure_ascii': False})
        
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Producto no encontrado'
            }, status=404)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

