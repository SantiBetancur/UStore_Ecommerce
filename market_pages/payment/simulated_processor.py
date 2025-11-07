import random
import uuid
import logging
from decimal import Decimal
from typing import Optional
from .payment_processor import PaymentProcessor, PaymentRequest, PaymentResult, PaymentStatus

logger = logging.getLogger(__name__)


class SimulatedPaymentProcessor(PaymentProcessor):
    """
    Procesador de pago simulado para desarrollo y testing.
    
    Simula diferentes escenarios de pago:
    - Pagos exitosos (80% probabilidad)
    - Pagos fallidos (15% probabilidad)
    - Pagos pendientes (5% probabilidad)
    """
    
    def __init__(self, success_rate: float = 0.80):
        """
        Inicializa el procesador simulado.
        
        Args:
            success_rate: Probabilidad de éxito (0.0 a 1.0). Por defecto 0.80 (80%)
        """
        self.success_rate = max(0.0, min(1.0, success_rate))
        self._available = True
    
    def process_payment(self, request: PaymentRequest) -> PaymentResult:
        """
        Simula el procesamiento de un pago.
        
        Args:
            request: Información del pago a procesar
        
        Returns:
            PaymentResult con el resultado simulado
        """
        logger.info(f"Simulando pago de {request.amount} {request.currency}")
        
        # Validaciones básicas
        if request.amount <= 0:
            return PaymentResult(
                success=False,
                status=PaymentStatus.FAILED,
                message="El monto debe ser mayor a cero",
                error_code="INVALID_AMOUNT"
            )
        
        # Generar ID de transacción simulado
        transaction_id = f"SIM-{uuid.uuid4().hex[:8].upper()}"
        
        # Simular procesamiento con delay
        import time
        time.sleep(0.5)  # Simular latencia de red
        
        # Determinar resultado basado en probabilidad
        random_value = random.random()
        
        if random_value <= self.success_rate:
            # Pago exitoso
            return PaymentResult(
                success=True,
                status=PaymentStatus.SUCCESS,
                transaction_id=transaction_id,
                message="Pago procesado exitosamente",
                metadata={
                    "processor": "simulated",
                    "simulated": True,
                    "processing_time_ms": 500
                }
            )
        elif random_value <= self.success_rate + 0.15:
            # Pago fallido
            failure_reasons = [
                "Fondos insuficientes",
                "Tarjeta rechazada",
                "Error de conexión con el banco",
                "Tarjeta vencida",
                "Límite de transacción excedido"
            ]
            return PaymentResult(
                success=False,
                status=PaymentStatus.FAILED,
                transaction_id=transaction_id,
                message=random.choice(failure_reasons),
                error_code="PAYMENT_FAILED",
                metadata={
                    "processor": "simulated",
                    "simulated": True
                }
            )
        else:
            # Pago pendiente
            return PaymentResult(
                success=False,
                status=PaymentStatus.PENDING,
                transaction_id=transaction_id,
                message="Pago en proceso, por favor espere confirmación",
                metadata={
                    "processor": "simulated",
                    "simulated": True,
                    "requires_confirmation": True
                }
            )
    
    def get_processor_name(self) -> str:
        """Retorna el nombre del procesador"""
        return "Simulated Payment Processor"
    
    def is_available(self) -> bool:
        """Verifica si el procesador está disponible"""
        return self._available
    
    def set_available(self, available: bool):
        """Permite cambiar manualmente la disponibilidad (útil para testing)"""
        self._available = available

