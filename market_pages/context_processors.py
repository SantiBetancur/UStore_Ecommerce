from .models.CartModel import CartItem

def cart_item_count(request):
    if not request.user.is_authenticated:
        return {"cart_item_count": 0}
    
    try:
        # Ojo: Campo correcto es buyer
        total_items = sum(item.quantity for item in CartItem.objects.filter(cart__buyer=request.user))
    except Exception:
        total_items = 0

    return {"cart_item_count": total_items}
