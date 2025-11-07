import requests
import logging
from typing import Dict, List, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class UrbanLoomAPIClient:
    """
    Cliente para consumir la API de UrbanLoom y obtener productos patrocinados.
    """
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000/catalog/api/products/", timeout: int = None):
        """
        Inicializa el cliente de la API de UrbanLoom.
        
        Args:
            base_url: URL base de la API de UrbanLoom
            timeout: Timeout en segundos (si no se proporciona, usa el de settings)
        """
        self.base_url = base_url
        if timeout is None:
            self.timeout = getattr(settings, 'URBANLOOM_API_TIMEOUT', 10)
        else:
            self.timeout = timeout
    
    def get_products(self, **kwargs) -> Dict:
        """
        Obtiene productos patrocinados de la API de UrbanLoom.
        
        Args:
            **kwargs: Parámetros opcionales para la petición (filtros, paginación, etc.)
        
        Returns:
            Dict con la respuesta de la API o None si hay error
        """
        try:
            response = requests.get(
                self.base_url,
                params=kwargs,
                timeout=self.timeout
            )
            response.raise_for_status()  # Lanza excepción para códigos de error HTTP
            return response.json()
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout al conectar con UrbanLoom API: {self.base_url}")
            return None
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Error de conexión con UrbanLoom API: {self.base_url}")
            return None
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"Error HTTP al consultar UrbanLoom API: {e.response.status_code} - {e}")
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error inesperado al consultar UrbanLoom API: {e}")
            return None
    
    def get_active_products(self) -> List[Dict]:
        """
        Obtiene solo los productos activos de UrbanLoom.
        
        Returns:
            Lista de productos activos
        """
        response = self.get_products()
        if not response or not response.get('success', False):
            return []
        
        products = response.get('products', [])
        # Filtrar solo productos activos
        active_products = [p for p in products if p.get('is_active', False)]
        return active_products
    
    @staticmethod
    def normalize_product(urbanloom_product: Dict) -> Dict:
        """
        Normaliza un producto de UrbanLoom al formato interno de UStore.
        
        Args:
            urbanloom_product: Producto en formato UrbanLoom
        
        Returns:
            Producto normalizado al formato UStore
        """
        # Extraer información de categoría
        category_info = urbanloom_product.get('category', {})
        if isinstance(category_info, dict):
            category_name = category_info.get('name', 'Sin categoría')
            category_id = category_info.get('id')
        else:
            # Si category es un string o otro tipo
            category_name = str(category_info) if category_info else 'Sin categoría'
            category_id = None
        
        # Extraer información de colección
        collection_info = urbanloom_product.get('collection')
        if isinstance(collection_info, dict):
            collection_name = collection_info.get('name', '')
            collection_id = collection_info.get('id')
        else:
            collection_name = None
            collection_id = None
        
        # Construir descripción mejorada
        description = urbanloom_product.get('description', '')
        if collection_name:
            description = f"{description} - Colección: {collection_name}"
        
        return {
            'id': urbanloom_product.get('id'),
            'name': urbanloom_product.get('name', ''),
            'description': description,
            'price': float(urbanloom_product.get('price', 0)),
            'stock': urbanloom_product.get('stock', 0),
            'is_active': urbanloom_product.get('is_active', False),
            'image': urbanloom_product.get('image', ''),
            'category': category_name,
            'category_id': category_id,
            'collection': collection_name,
            'collection_id': collection_id,
            'created_at': urbanloom_product.get('created_at', ''),
            'source': 'urbanloom',  # Marca que viene de UrbanLoom
            'is_sponsored': True,  # Indica que es un producto patrocinado
        }


# Instancia global del cliente (puede configurarse desde settings.py)
def get_urbanloom_client() -> UrbanLoomAPIClient:
    """
    Obtiene una instancia del cliente de UrbanLoom API.
    Puede configurarse desde settings.py usando URBANLOOM_API_URL y URBANLOOM_API_TIMEOUT.
    """
    api_url = getattr(settings, 'URBANLOOM_API_URL', 'http://127.0.0.1:8000/catalog/api/products/')
    timeout = getattr(settings, 'URBANLOOM_API_TIMEOUT', 10)
    return UrbanLoomAPIClient(base_url=api_url, timeout=timeout)
