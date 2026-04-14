// ============================================
// COMPONENTE TARJETAS (CARDS)
// ============================================

class CardComponent {
    // Crear tarjeta de estadísticas
    static createStatCard(title, value, icon, color = 'primary', onClick = null) {
        const colors = {
            primary: 'bg-primary',
            success: 'bg-success',
            danger: 'bg-danger',
            warning: 'bg-warning',
            info: 'bg-info',
            dark: 'bg-dark'
        };
        
        const card = document.createElement('div');
        card.className = 'card card-dashboard';
        if (onClick) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', onClick);
        }
        
        card.innerHTML = `
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="card-title">${title}</h6>
                        <h3 class="card-value">${value}</h3>
                    </div>
                    <div class="card-icon ${colors[color]}">
                        <i class="fas ${icon}"></i>
                    </div>
                </div>
            </div>
        `;
        
        return card;
    }
    
    // Crear tarjeta de información
    static createInfoCard(title, content, icon = 'fa-info-circle') {
        const card = document.createElement('div');
        card.className = 'info-card';
        
        card.innerHTML = `
            <h5><i class="fas ${icon} me-2 text-primary"></i>${title}</h5>
            <hr>
            ${content}
        `;
        
        return card;
    }
    
    // Crear tarjeta con imagen
    static createImageCard(title, description, imageUrl, buttonText = 'Ver más', onButtonClick = null) {
        const card = document.createElement('div');
        card.className = 'card h-100';
        
        card.innerHTML = `
            <img src="${imageUrl}" class="card-img-top" alt="${title}" style="height: 200px; object-fit: cover;">
            <div class="card-body">
                <h5 class="card-title">${title}</h5>
                <p class="card-text">${description}</p>
                <button class="btn btn-primary btn-sm">${buttonText}</button>
            </div>
        `;
        
        if (onButtonClick) {
            card.querySelector('.btn').addEventListener('click', onButtonClick);
        }
        
        return card;
    }
    
    // Crear tarjeta de progreso
    static createProgressCard(title, percentage, color = 'success') {
        const card = document.createElement('div');
        card.className = 'card mb-3';
        
        card.innerHTML = `
            <div class="card-body">
                <h6 class="card-title">${title}</h6>
                <div class="progress mb-2">
                    <div class="progress-bar bg-${color}" style="width: ${percentage}%"></div>
                </div>
                <small class="text-muted">${percentage}% completado</small>
            </div>
        `;
        
        return card;
    }
}

// Función para actualizar tarjeta de estadísticas
function updateStatCard(cardElement, newValue) {
    const valueElement = cardElement.querySelector('.card-value');
    if (valueElement) {
        valueElement.textContent = newValue;
    }
}