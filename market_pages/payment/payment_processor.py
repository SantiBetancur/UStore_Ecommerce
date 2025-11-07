from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from decimal import Decimal


class PaymentStatus(Enum):
    """Estados posibles de un pago"""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    CANCELLED = "cancelled"


@dataclass
class PaymentRequest:
    """Solicitud de pago"""
    amount: Decimal
    currency: str = "COP"
    order_id: Optional[str] = None
    customer_email: Optional[str] = None
    customer_name: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[dict] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class PaymentResult:
    """Resultado de un procesamiento de pago"""
    success: bool
    status: PaymentStatus
    transaction_id: Optional[str] = None
    message: Optional[str] = None
    error_code: Optional[str] = None
    metadata: Optional[dict] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class PaymentProcessor(ABC):
    """
    Interfaz abstracta para procesadores de pago.
    
    Este es el contrato que todos los procesadores de pago deben implementar.
    La vista depende de esta abstracción, no de implementaciones concretas,
    aplicando el Principio de Inversión de Dependencias (DIP).
    """
    
    @abstractmethod
    def process_payment(self, request: PaymentRequest) -> PaymentResult:
        """
        Procesa un pago.
        
        Args:
            request: Información del pago a procesar
        
        Returns:
            PaymentResult con el resultado del procesamiento
        """
        pass
    
    @abstractmethod
    def get_processor_name(self) -> str:
        """
        Retorna el nombre del procesador de pago.
        
        Returns:
            Nombre del procesador
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica si el procesador está disponible.
        
        Returns:
            True si el procesador está disponible, False en caso contrario
        """
        pass

