from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.db import transaction
import logging

from ..models.CartModel import Cart
from ..payment import PaymentService
from ..payment.payment_factory import get_payment_processor

logger = logging.getLogger(__name__)


class PaymentView(View):
    """
    Vista para procesar el pago de un carrito.
    
    Esta vista aplica el Principio de Inversión de Dependencias al:
    1. Obtener el procesador de pago a través de un factory
    2. Inyectar el procesador en el PaymentService
    3. No depender directamente de implementaciones concretas de procesadores
    """
    template_name = 'pages/payment.html'
    
    def dispatch(self, request, *args, **kwargs):
        """Verifica autenticación antes de procesar"""
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        """
        Muestra la página de confirmación de pago.
        """
        try:
            cart = get_object_or_404(Cart, buyer=request.user)
            
            # Verificar que el carrito no esté vacío
            if cart.items.count() == 0:
                messages.warning(request, "Tu carrito está vacío")
                return redirect('view_cart')
            
            total = cart.total()
            
            context = {
                'cart': cart,
                'total': total,
                'page_title': 'Procesar Pago - UStore',
                'username': request.session.get('username', ''),
                'user': request.user,
                'cart_count': request.session.get('cart_count', 0),
            }
            
            return render(request, self.template_name, context)
        
        except Cart.DoesNotExist:
            messages.error(request, "No se encontró tu carrito")
            return redirect('view_cart')
        except Exception as e:
            logger.error(f"Error al mostrar página de pago: {e}")
            messages.error(request, "Ocurrió un error al cargar la página de pago")
            return redirect('view_cart')
    
    def post(self, request):
        """
        Procesa el pago del carrito.
        
        Aplica el principio de Inversión de Dependencias:
        - Obtiene el procesador a través del factory (no depende de implementación concreta)
        - Inyecta el procesador en el PaymentService
        - El servicio procesa el pago sin conocer la implementación específica
        """
        try:
            cart = get_object_or_404(Cart, buyer=request.user)
            
            # Verificar que el carrito no esté vacío
            if cart.items.count() == 0:
                messages.warning(request, "Tu carrito está vacío")
                return redirect('view_cart')
            
            # Obtener procesador de pago mediante factory (aplicando DIP)
            payment_processor = get_payment_processor()
            
            # Inyectar procesador en el servicio (inyección de dependencias)
            payment_service = PaymentService(payment_processor)
            
            # Procesar el pago
            result = payment_service.process_cart_payment(cart)
            
            if result.success:
                # Pago exitoso: limpiar carrito y redirigir
                with transaction.atomic():
                    cart.clear()
                    request.session['cart_count'] = 0
                
                messages.success(
                    request,
                    f"¡Pago procesado exitosamente! ID de transacción: {result.transaction_id}"
                )
                logger.info(f"Pago exitoso para usuario {request.user.pk}. Transaction: {result.transaction_id}")
                return redirect('payment_success')
            else:
                # Pago fallido: mostrar error
                error_message = result.message or "El pago no pudo ser procesado"
                messages.error(request, f"Error en el pago: {error_message}")
                logger.warning(f"Pago fallido para usuario {request.user.pk}: {error_message}")
                return redirect('view_cart')
        
        except Cart.DoesNotExist:
            messages.error(request, "No se encontró tu carrito")
            return redirect('view_cart')
        except Exception as e:
            logger.error(f"Error al procesar pago: {e}", exc_info=True)
            messages.error(request, "Ocurrió un error inesperado al procesar el pago")
            return redirect('view_cart')


class PaymentSuccessView(View):
    """Vista para mostrar la confirmación de pago exitoso"""
    template_name = 'pages/payment_success.html'
    
    def get(self, request):
        context = {
            'page_title': 'Pago Exitoso - UStore',
            'username': request.session.get('username', ''),
            'user': request.user,
        }
        return render(request, self.template_name, context)

