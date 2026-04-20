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
        this.duration = parseInt(this.getAttribute('duration')) || 3000;
        this.render();
    }
    
    render() {
        const types = {
            success: { icon: '✅', color: '#27ae60', bg: '#d4edda', title: 'Éxito' },
            error: { icon: '❌', color: '#e74c3c', bg: '#f8d7da', title: 'Error' },
            warning: { icon: '⚠️', color: '#f39c12', bg: '#fff3cd', title: 'Advertencia' },
            info: { icon: 'ℹ️', color: '#3498db', bg: '#d1ecf1', title: 'Información' }
        };
        const current = types[this.type] || types.info;
        this.shadowRoot.innerHTML = `
            <style>
                .alert { position: fixed; top: 20px; right: 20px; min-width: 300px; padding: 15px 20px; border-radius: 8px; background: ${current.bg}; border-left: 4px solid ${current.color}; box-shadow: 0 4px 12px rgba(0,0,0,0.15); display: flex; align-items: center; gap: 12px; font-family: 'Segoe UI', sans-serif; z-index: 10000; animation: slideIn 0.3s ease; }
                @keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
                @keyframes slideOut { from { transform: translateX(0); opacity: 1; } to { transform: translateX(100%); opacity: 0; } }
                .icon { font-size: 24px; }
                .content { flex: 1; }
                .title { font-weight: bold; color: ${current.color}; margin-bottom: 4px; }
                .message { color: #333; font-size: 14px; }
                .close { background: none; border: none; font-size: 20px; cursor: pointer; color: #999; transition: color 0.2s; }
                .close:hover { color: #333; }
            </style>
            <div class="alert"><span class="icon">${current.icon}</span><div class="content"><div class="title">${current.title}</div><div class="message">${this.message}</div></div><button class="close">&times;</button></div>
        `;
        this.shadowRoot.querySelector('.close')?.addEventListener('click', () => this.close());
        if (this.duration > 0) this.timeout = setTimeout(() => this.close(), this.duration);
    }
    
    close() {
        const alert = this.shadowRoot.querySelector('.alert');
        if (alert) { alert.style.animation = 'slideOut 0.3s ease'; setTimeout(() => this.remove(), 300); }
        if (this.timeout) clearTimeout(this.timeout);
    }
    
    static show(type, message, duration = 3000) {
        const alert = document.createElement('custom-alert');
        alert.setAttribute('type', type);
        alert.setAttribute('message', message);
        alert.setAttribute('duration', duration);
        document.body.appendChild(alert);
        return alert;
    }
}
customElements.define('custom-alert', CustomAlert);
window.showAlert = (message, type = 'success') => CustomAlert.show(type, message);