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
    return render(request, 'pages/favorites_list.html', {'products': products})
