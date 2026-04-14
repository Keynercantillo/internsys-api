// ============================================
// COMPONENTE DE ALERTAS
// ============================================

const AlertComponent = {
    // Mostrar alerta
    show(message, type = 'success', duration = 3000) {
        // Eliminar alertas existentes
        const existingAlerts = document.querySelectorAll('.alert-custom');
        existingAlerts.forEach(alert => alert.remove());
        
        // Crear nueva alerta
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-custom shadow-lg`;
        
        // Configurar estilos
        alertDiv.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            min-width: 320px;
            z-index: 9999;
            animation: slideInRight 0.3s ease;
            border-left: 4px solid ${type === 'success' ? '#27ae60' : type === 'danger' ? '#e74c3c' : type === 'warning' ? '#f39c12' : '#3498db'};
            background: white;
            border-radius: 8px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        `;
        
        // Iconos según tipo
        const icons = {
            success: 'fa-check-circle',
            danger: 'fa-exclamation-circle',
            warning: 'fa-exclamation-triangle',
            info: 'fa-info-circle'
        };
        
        const colors = {
            success: '#27ae60',
            danger: '#e74c3c',
            warning: '#f39c12',
            info: '#3498db'
        };
        
        alertDiv.innerHTML = `
            <div class="d-flex align-items-center p-3">
                <i class="fas ${icons[type]} me-3 fa-lg" style="color: ${colors[type]}"></i>
                <div class="flex-grow-1" style="color: #333;">${message}</div>
                <button type="button" class="btn-close ms-3" onclick="this.closest('.alert-custom').remove()" style="font-size: 12px;"></button>
            </div>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto cerrar después de duración
        setTimeout(() => {
            if (alertDiv && alertDiv.remove) {
                alertDiv.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => alertDiv.remove(), 300);
            }
        }, duration);
    },
    
    // Alerta de éxito
    success(message, duration = 3000) {
        this.show(message, 'success', duration);
    },
    
    // Alerta de error
    error(message, duration = 4000) {
        this.show(message, 'danger', duration);
    },
    
    // Alerta de advertencia
    warning(message, duration = 3500) {
        this.show(message, 'warning', duration);
    },
    
    // Alerta de información
    info(message, duration = 3000) {
        this.show(message, 'info', duration);
    },
    
    // Alerta de confirmación
    confirm(message, onConfirm, onCancel) {
        const confirmDiv = document.createElement('div');
        confirmDiv.className = 'alert alert-warning alert-custom shadow-lg';
        confirmDiv.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            min-width: 320px;
            z-index: 9999;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #f39c12;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        `;
        
        confirmDiv.innerHTML = `
            <div class="p-3">
                <div class="d-flex align-items-center mb-3">
                    <i class="fas fa-question-circle me-3 fa-lg" style="color: #f39c12"></i>
                    <div class="flex-grow-1" style="color: #333;">${message}</div>
                </div>
                <div class="d-flex justify-content-end gap-2">
                    <button class="btn btn-sm btn-secondary" onclick="this.closest('.alert-custom').remove()">Cancelar</button>
                    <button class="btn btn-sm btn-warning" id="confirmBtn">Confirmar</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(confirmDiv);
        
        document.getElementById('confirmBtn').addEventListener('click', () => {
            confirmDiv.remove();
            if (onConfirm) onConfirm();
        });
    }
};

// Agregar animación de salida
if (!document.querySelector('#alertAnimationStyles')) {
    const style = document.createElement('style');
    style.id = 'alertAnimationStyles';
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}