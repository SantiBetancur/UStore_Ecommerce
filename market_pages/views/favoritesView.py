from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from market_pages.models.favoriteModel import Favorite
from market_pages.models.ProductModel import Product

@login_required
def toggle_favorite(request, product_id):
    """Agrega o quita un producto de favoritos y redirige a la lista de favoritos."""
    product = Product.objects.filter(id=product_id).first()
    if not product:
        # Si el producto no existe, también redirigimos a favoritos
        return redirect('favorite_list')

    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
    
    # Siempre redirigimos a la página de favoritos
    return redirect('favorite_list')


@login_required
def favorite_list(request):
    """Muestra los productos favoritos del usuario."""
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    products = [fav.product for fav in favorites]
    
    # Obtener variables para el navbar (ya están disponibles globalmente por context processor,
    # pero las incluimos aquí por si acaso)
    username = request.session.get('username', '')
    storename = request.session.get('short_storename', '') if request.session.get('short_storename', '') else "Mi tienda"
    cart_count = request.session.get('cart_count', 0)
    
    context = {
        'products': products,
        'page_title': 'Mis Favoritos - UStore',
        'username': username,
        'storename': storename,
        'cart_count': cart_count,
        'user': request.user,
    }
    
    return render(request, 'pages/favorites_list.html', context)
