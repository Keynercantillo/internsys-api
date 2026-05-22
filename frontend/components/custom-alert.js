// components/custom-alert.js
class CustomAlert extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.timeout = null;
    }
    
    connectedCallback() {
        this.type = this.getAttribute('type') || 'info';
        this.message = this.getAttribute('message') || '';
        this.title = this.getAttribute('title') || '';
        this.duration = parseInt(this.getAttribute('duration')) || 3000;
        this.render();
    }
    
    render() {
        const types = {
            success: { 
                icon: '✅', 
                color: '#27ae60', 
                bg: '#d4edda', 
                borderColor: '#27ae60',
                defaultTitle: 'Éxito' 
            },
            error: { 
                icon: '❌', 
                color: '#e74c3c', 
                bg: '#f8d7da', 
                borderColor: '#e74c3c',
                defaultTitle: 'Error' 
            },
            warning: { 
                icon: '⚠️', 
                color: '#f39c12', 
                bg: '#fff3cd', 
                borderColor: '#f39c12',
                defaultTitle: 'Advertencia' 
            },
            info: { 
                icon: 'ℹ️', 
                color: '#3498db', 
                bg: '#d1ecf1', 
                borderColor: '#3498db',
                defaultTitle: 'Información' 
            }
        };
        
        const current = types[this.type] || types.info;
        const alertTitle = this.title || current.defaultTitle;
        
        this.shadowRoot.innerHTML = `
            <style>
                .alert { 
                    position: fixed; 
                    top: 20px; 
                    right: 20px; 
                    min-width: 320px; 
                    max-width: 450px;
                    padding: 16px 20px; 
                    border-radius: 12px; 
                    background: ${current.bg}; 
                    border-left: 4px solid ${current.borderColor}; 
                    box-shadow: 0 8px 20px rgba(0,0,0,0.15); 
                    display: flex; 
                    align-items: center; 
                    gap: 14px; 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    z-index: 10000; 
                    animation: slideInRight 0.3s ease;
                    backdrop-filter: blur(4px);
                }
                @keyframes slideInRight { 
                    from { transform: translateX(100%); opacity: 0; } 
                    to { transform: translateX(0); opacity: 1; } 
                }
                @keyframes slideOutRight { 
                    from { transform: translateX(0); opacity: 1; } 
                    to { transform: translateX(100%); opacity: 0; } 
                }
                .icon { 
                    font-size: 28px; 
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .content { 
                    flex: 1; 
                }
                .title { 
                    font-weight: bold; 
                    color: ${current.color}; 
                    margin-bottom: 4px; 
                    font-size: 16px;
                }
                .message { 
                    color: #333; 
                    font-size: 13px; 
                    line-height: 1.4;
                }
                .close { 
                    background: none; 
                    border: none; 
                    font-size: 20px; 
                    cursor: pointer; 
                    color: #999; 
                    transition: color 0.2s;
                    padding: 0;
                    width: 24px;
                    height: 24px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                }
                .close:hover { 
                    color: #333; 
                    background: rgba(0,0,0,0.05);
                }
            </style>
            <div class="alert">
                <span class="icon">${current.icon}</span>
                <div class="content">
                    <div class="title">${alertTitle}</div>
                    <div class="message">${this.message}</div>
                </div>
                <button class="close">&times;</button>
            </div>
        `;
        
        this.shadowRoot.querySelector('.close')?.addEventListener('click', () => this.close());
        if (this.duration > 0) {
            this.timeout = setTimeout(() => this.close(), this.duration);
        }
    }
    
    close() {
        const alert = this.shadowRoot.querySelector('.alert');
        if (alert) { 
            alert.style.animation = 'slideOutRight 0.3s ease'; 
            setTimeout(() => this.remove(), 300); 
        }
        if (this.timeout) clearTimeout(this.timeout);
    }
    
    static show(type, message, title = '', duration = 3000) {
        const alert = document.createElement('custom-alert');
        alert.setAttribute('type', type);
        alert.setAttribute('message', message);
        if (title) alert.setAttribute('title', title);
        alert.setAttribute('duration', duration);
        document.body.appendChild(alert);
        return alert;
    }
    
    static success(message, title = 'Éxito', duration = 3000) {
        return CustomAlert.show('success', message, title, duration);
    }
    
    static error(message, title = 'Error', duration = 3000) {
        return CustomAlert.show('error', message, title, duration);
    }
    
    static warning(message, title = 'Advertencia', duration = 3000) {
        return CustomAlert.show('warning', message, title, duration);
    }
    
    static info(message, title = 'Información', duration = 3000) {
        return CustomAlert.show('info', message, title, duration);
    }
}

customElements.define('custom-alert', CustomAlert);

// Función global para compatibilidad con código existente
window.showAlert = (message, type = 'success') => {
    if (type === 'success') CustomAlert.success(message);
    else if (type === 'error') CustomAlert.error(message);
    else if (type === 'warning') CustomAlert.warning(message);
    else CustomAlert.info(message);
};

// Función para mostrar mensaje de bienvenida (como en tu imagen)
window.showWelcomeAlert = (userName, userRole) => {
    let roleText = '';
    if (userRole === 'admin') roleText = 'Administrador';
    else if (userRole === 'estudiante') roleText = 'Estudiante';
    else if (userRole === 'empresa') roleText = 'Empresa';
    else if (userRole === 'tutor') roleText = 'Tutor';
    
    CustomAlert.success(
        `<div style="text-align: center;">
            <strong style="font-size: 18px;">${userName}</strong><br>
            <span style="font-size: 12px;">(${roleText})</span>
        </div>`,
        'Bienvenido',
        4000
    );
};

// Función para confirmar antes de eliminar
window.confirmDelete = (itemName, callback) => {
    // Crear una alerta de confirmación personalizada
    const confirmDiv = document.createElement('div');
    confirmDiv.className = 'confirm-dialog';
    confirmDiv.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 10001;">
            <div style="background: white; border-radius: 16px; padding: 24px; min-width: 320px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.2);">
                <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
                <h3 style="margin-bottom: 12px; color: #2c3e50;">¿Eliminar?</h3>
                <p style="margin-bottom: 24px; color: #7f8c8d;">¿Estás seguro de eliminar ${itemName}?</p>
                <div style="display: flex; gap: 12px; justify-content: center;">
                    <button id="confirmCancel" style="background: #95a5a6; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">Cancelar</button>
                    <button id="confirmOk" style="background: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">Eliminar</button>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(confirmDiv);
    
    document.getElementById('confirmOk').onclick = () => {
        confirmDiv.remove();
        callback();
    };
    document.getElementById('confirmCancel').onclick = () => confirmDiv.remove();
}; 