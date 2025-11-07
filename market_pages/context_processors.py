def cart_item_count(request):
    """Context processor para el contador de items en el carrito"""
    from .models.CartModel import CartItem
    
    if not request.user.is_authenticated:
        return {
            "cart_item_count": 0,
            "cart_count": 0,
        }
    
    try:
        # Ojo: Campo correcto es buyer
        total_items = sum(item.quantity for item in CartItem.objects.filter(cart__buyer=request.user))
        # Actualizar la sesión
        request.session['cart_count'] = total_items
    except Exception:
        total_items = 0

    return {
        "cart_item_count": total_items,
        "cart_count": total_items,  # Alias para compatibilidad con el navbar
    }


def navbar_context(request):
    """Context processor para variables del navbar (username, storename, etc.)"""
    context = {
        'username': '',
        'storename': 'Mi tienda',
        'cart_count': 0,
    }
    
    if request.user.is_authenticated:
        # Obtener username de la sesión o del usuario
        username = request.session.get('username', '')
        if not username and hasattr(request.user, 'name'):
            username = (request.user.name[:20] + '...') if len(request.user.name) > 20 else request.user.name
            request.session['username'] = username
        
        # Obtener storename de la sesión
        storename = request.session.get('short_storename', '')
        if not storename:
            if hasattr(request.user, 'store') and request.user.store:
                storename = request.user.store.name[:20] + '...' if len(request.user.store.name) > 20 else request.user.store.name
                request.session['short_storename'] = storename
            else:
                storename = 'Mi tienda'
        
        # Obtener cart_count de la sesión o calcularlo
        cart_count = request.session.get('cart_count', 0)
        if cart_count == 0:
            try:
                from .models.CartModel import CartItem
                cart_count = sum(item.quantity for item in CartItem.objects.filter(cart__buyer=request.user))
                request.session['cart_count'] = cart_count
            except Exception:
                cart_count = 0
        
        context.update({
            'username': username,
            'storename': storename,
            'cart_count': cart_count,
        })
    
    return context
