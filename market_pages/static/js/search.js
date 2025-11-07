document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    const searchResultsList = document.getElementById('searchResultsList');
    let searchTimeout;

    // Función para realizar la búsqueda
    function performSearch(query) {
        if (query.length < 2) {
            searchResults.style.display = 'none';
            return;
        }

        fetch(`/search/?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySearchResults(data.products);
            })
            .catch(error => {
                console.error('Error en la búsqueda:', error);
            });
    }

    // Función para mostrar los resultados
    function displaySearchResults(products) {
        if (products.length === 0) {
            searchResultsList.innerHTML = '<div class="search-result-item text-muted">No se encontraron productos</div>';
        } else {
            searchResultsList.innerHTML = products.map(product => `
                <div class="search-result-item" onclick="window.location.href='${product.url}'">
                    <div class="search-result-image">
                        <img src="${product.image_url}" alt="${product.name}" class="rounded">
                    </div>
                    <div class="search-result-info">
                        <h6 class="search-result-name">${product.name}</h6>
                        <small class="search-result-category">${product.category} • ${product.type}</small>
                        <div class="search-result-price">$${product.price.toLocaleString()}</div>
                    </div>
                </div>
            `).join('');
        }
        searchResults.style.display = 'block';
    }

    // Event listener para el input de búsqueda
    searchInput.addEventListener('input', function() {
        const query = this.value.trim();
        
        // Limpiar timeout anterior
        clearTimeout(searchTimeout);
        
        // Establecer nuevo timeout para evitar muchas requests
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });

    // Ocultar resultados cuando se hace clic fuera
    document.addEventListener('click', function(event) {
        if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
            searchResults.style.display = 'none';
        }
    });

    // Mostrar resultados cuando se hace foco en el input
    searchInput.addEventListener('focus', function() {
        if (this.value.trim().length >= 2) {
            searchResults.style.display = 'block';
        }
    });
});