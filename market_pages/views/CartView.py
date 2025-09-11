from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from market_pages.models.CartModel import Cart, CartItem
from market_pages.models.ProductModel import Product

#@login_required
def view_cart(request):
    template_name = "pages/cart.html"
    if not request.user.is_authenticated:
        return redirect("login")

    cart, created = Cart.objects.get_or_create(buyer=request.user)
    # Bring the username from the session
    username = request.session.get('username', '') if request.user.is_authenticated else ''
    context = {
        'cart': cart,
        'page_title': 'Mi Carrito - UStore',
        'username': username,
        'user': request.user,
    }
    return render(request, template_name, context)

#@login_required
def add_to_cart(request, product_id):
    template_name = "pages/cart.html"
    if not request.user.is_authenticated:
        return redirect("login")
    cart, created = Cart.objects.get_or_create(buyer=request.user)
    product = get_object_or_404(Product, id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    return redirect("view_cart")

#@login_required
def remove_from_cart(request, item_id):
    template_name = "pages/cart.html"
    item = get_object_or_404(CartItem, id=item_id, cart__buyer=request.user)
    item.delete()
    return redirect("view_cart")

#@login_required
def clear_cart(request):
    template_name = "pages/cart.html"
    cart, created = Cart.objects.get_or_create(buyer=request.user)
    cart.clear()
    return redirect("view_cart")
