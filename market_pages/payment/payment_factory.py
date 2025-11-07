from django.conf import settings
import logging
from .payment_processor import PaymentProcessor
from .simulated_processor import SimulatedPaymentProcessor

logger = logging.getLogger(__name__)


def get_payment_processor() -> PaymentProcessor:
    """
    Factory function que retorna el procesador de pago configurado.
    
    Esta función implementa el patrón Factory para crear instancias
    del procesador de pago según la configuración en settings.py.
    Aplica el principio de Inversión de Dependencias al depender
    de la abstracción PaymentProcessor.
    
    Returns:
        Instancia de PaymentProcessor configurada
    """
    processor_type = getattr(settings, 'PAYMENT_PROCESSOR', 'simulated').lower()
    
    if processor_type == 'simulated':
        success_rate = getattr(settings, 'SIMULATED_PAYMENT_SUCCESS_RATE', 0.80)
        return SimulatedPaymentProcessor(success_rate=success_rate)
    
    # Aquí se pueden agregar más procesadores en el futuro:
    # elif processor_type == 'stripe':
    #     return StripePaymentProcessor(...)
    # elif processor_type == 'paypal':
    #     return PayPalPaymentProcessor(...)
    
    else:
        logger.warning(f"Procesador de pago '{processor_type}' no reconocido. Usando procesador simulado.")
        return SimulatedPaymentProcessor()

