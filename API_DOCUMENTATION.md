# API REST - Productos UStore

Esta documentación describe los endpoints disponibles para consumir información de productos a través de HTTP.

## Base URL
```
http://localhost:8000/api/products/
```

## Endpoints

### 1. Listar Productos
Obtiene una lista de todos los productos disponibles con todos sus atributos.

**Endpoint:** `GET /api/products/`

**Parámetros de consulta (opcionales):**
- `category`: Filtrar por categoría (búsqueda parcial, case-insensitive)
- `type`: Filtrar por tipo (`product` o `service`)
- `store_id`: Filtrar por ID de tienda
- `min_price`: Precio mínimo
- `max_price`: Precio máximo
- `search`: Buscar en nombre, categoría, tipo o descripción
- `limit`: Número máximo de resultados (default: 100, máximo: 1000)
- `offset`: Offset para paginación (default: 0)

**Ejemplo de petición:**
```bash
GET http://localhost:8000/api/products/?category=Electronics&min_price=1000&limit=10
```

**Ejemplo de respuesta:**
```json
{
    "success": true,
    "total": 25,
    "limit": 10,
    "offset": 0,
    "count": 10,
    "products": [
        {
            "id": 1,
            "name": "Laptop HP",
            "category": "Electronics",
            "type": "product",
            "description": "Laptop de alta gama con procesador Intel i7",
            "price": 1500000.0,
            "image_url": "http://localhost:8000/media/products/laptop.jpg",
            "created_at": "2025-11-06T14:30:00.123456",
            "updated_at": "2025-11-06T14:30:00.123456",
            "store": {
                "id": 1,
                "name": "TechStore",
                "description": "Tienda de tecnología",
                "logo": "https://example.com/logo.png"
            }
        }
    ]
}
```

### 2. Obtener Producto por ID
Obtiene los detalles de un producto específico por su ID.

**Endpoint:** `GET /api/products/{product_id}/`

**Ejemplo de petición:**
```bash
GET http://localhost:8000/api/products/1/
```

**Ejemplo de respuesta:**
```json
{
    "success": true,
    "product": {
        "id": 1,
        "name": "Laptop HP",
        "category": "Electronics",
        "type": "product",
        "description": "Laptop de alta gama con procesador Intel i7",
        "price": 1500000.0,
        "image_url": "http://localhost:8000/media/products/laptop.jpg",
        "created_at": "2025-11-06T14:30:00.123456",
        "updated_at": "2025-11-06T14:30:00.123456",
        "store": {
            "id": 1,
            "name": "TechStore",
            "description": "Tienda de tecnología",
            "logo": "https://example.com/logo.png"
        }
    }
}
```

**Códigos de estado:**
- `200`: Éxito
- `404`: Producto no encontrado
- `400`: Error en los parámetros
- `500`: Error interno del servidor

## Ejemplos de Uso

### Ejemplo 1: Obtener todos los productos
```bash
curl http://localhost:8000/api/products/
```

### Ejemplo 2: Filtrar por categoría
```bash
curl http://localhost:8000/api/products/?category=Electronics
```

### Ejemplo 3: Buscar productos
```bash
curl http://localhost:8000/api/products/?search=laptop
```

### Ejemplo 4: Filtrar por rango de precios
```bash
curl http://localhost:8000/api/products/?min_price=1000&max_price=50000
```

### Ejemplo 5: Paginación
```bash
curl http://localhost:8000/api/products/?limit=20&offset=40
```

### Ejemplo 6: Combinar múltiples filtros
```bash
curl "http://localhost:8000/api/products/?category=Electronics&type=product&min_price=1000&limit=10"
```

## Estructura de Respuesta

### Lista de Productos
```json
{
    "success": boolean,
    "total": number,          // Total de productos que cumplen los filtros
    "limit": number,          // Límite aplicado
    "offset": number,         // Offset aplicado
    "count": number,          // Número de productos en esta respuesta
    "products": [             // Array de productos
        {
            "id": number,
            "name": string,
            "category": string,
            "type": string,
            "description": string,
            "price": number,
            "image_url": string | null,
            "created_at": string,     // ISO 8601 format
            "updated_at": string,     // ISO 8601 format
            "store": {                // null si no tiene tienda asociada
                "id": number,
                "name": string,
                "description": string,
                "logo": string | null
            }
        }
    ]
}
```

### Producto Individual
```json
{
    "success": boolean,
    "product": {
        // Misma estructura que un elemento del array "products"
    }
}
```

### Errores
```json
{
    "success": false,
    "error": "Mensaje de error descriptivo"
}
```

## Notas

1. Todas las respuestas están en formato JSON con codificación UTF-8.
2. Las URLs de imágenes incluyen el protocolo y host completo.
3. Los precios están en formato decimal (float).
4. Las fechas están en formato ISO 8601.
5. Si un producto no tiene tienda asociada, el campo `store` será `null`.
6. Los filtros son opcionales y pueden combinarse.
7. La búsqueda (`search`) busca en nombre, categoría, tipo y descripción.
8. El límite máximo es 1000 productos por petición.

