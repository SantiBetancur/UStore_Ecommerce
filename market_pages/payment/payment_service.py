from typing import Optional
from decimal import Decimal
import logging
from .payment_processor import PaymentProcessor, PaymentRequest, PaymentResult, PaymentStatus
from ..models.CartModel import Cart

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Servicio de pago que utiliza el principio de Inversión de Dependencias.
    
    Este servicio depende de la abstracción PaymentProcessor, no de implementaciones
    concretas. El procesador se inyecta en el constructor, permitiendo cambiar
    fácilmente entre diferentes proveedores de pago sin modificar este código.
    """
    
    def __init__(self, payment_processor: PaymentProcessor):
        """
        Inicializa el servicio de pago con un procesador inyectado.
        
        Args:
            payment_processor: Implementación de PaymentProcessor a utilizar
        """
        if not isinstance(payment_processor, PaymentProcessor):
            raise TypeError(
                "payment_processor debe ser una instancia de PaymentProcessor"
            )
        self._processor = payment_processor
        logger.info(f"PaymentService inicializado con procesador: {self._processor.get_processor_name()}")
    
    def process_cart_payment(self, cart: Cart) -> PaymentResult:
        """
        Procesa el pago de un carrito de compras.
        
        Args:
            cart: Carrito de compras a pagar
        
        Returns:
            PaymentResult con el resultado del pago
        """
        if not cart:
            return PaymentResult(
                success=False,
                status=PaymentStatus.FAILED,
                message="Carrito no válido",
                error_code="INVALID_CART"
            )
        
        # Verificar que el procesador esté disponible
        if not self._processor.is_available():
            return PaymentResult(
                success=False,
                status=PaymentStatus.FAILED,
                message="Procesador de pago no disponible",
                error_code="PROCESSOR_UNAVAILABLE"
            )
        
        # Calcular total del carrito
        total = cart.total()
        
        if total <= 0:
            return PaymentResult(
                success=False,
                status=PaymentStatus.FAILED,
                message="El carrito está vacío o el total es cero",
                error_code="EMPTY_CART"
            )
        
        # Crear solicitud de pago
        buyer_id = None
        if cart.buyer:
            # Usar pk que es genérico y funciona con cualquier clave primaria (id, user_id, etc.)
            buyer_id = cart.buyer.pk
        
        payment_request = PaymentRequest(
            amount=Decimal(str(total)),
            currency="COP",
            order_id=f"CART-{cart.id}",
            customer_email=cart.buyer.email if cart.buyer else None,
            customer_name=cart.buyer.name if hasattr(cart.buyer, 'name') else None,
            description=f"Pago de carrito #{cart.id}",
            metadata={
                "cart_id": cart.id,
                "buyer_id": buyer_id,
                "items_count": cart.items.count(),
            }
        )
        
        # Procesar el pago usando el procesador inyectado
        logger.info(f"Procesando pago para carrito #{cart.id} por ${total}")
        result = self._processor.process_payment(payment_request)
        
        if result.success:
            logger.info(f"Pago exitoso. Transaction ID: {result.transaction_id}")
        else:
            logger.warning(f"Pago fallido: {result.message}")
        
        return result
    
    def get_processor_name(self) -> str:
        """Retorna el nombre del procesador actual"""
        return self._processor.get_processor_name()

