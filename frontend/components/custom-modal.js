// components/custom-modal.js
class CustomModal extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.isOpen = false;
    }
    
    connectedCallback() {
        this.title = this.getAttribute('title') || 'Modal';
        this.size = this.getAttribute('size') || 'md';
        this.render();
    }
    
    render() {
        const sizes = { sm: 'width: 400px;', md: 'width: 600px;', lg: 'width: 800px;', xl: 'width: 90%; max-width: 1200px;' };
        this.shadowRoot.innerHTML = `
            <style>
                .overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: none; justify-content: center; align-items: center; z-index: 9999; font-family: 'Segoe UI', sans-serif; }
                .overlay.open { display: flex; }
                .modal { background: white; border-radius: 12px; ${sizes[this.size]} max-width: 90%; max-height: 90%; overflow: hidden; animation: fadeIn 0.2s ease; }
                @keyframes fadeIn { from { opacity: 0; transform: scale(0.9); } to { opacity: 1; transform: scale(1); } }
                .header { background: linear-gradient(135deg, #3498db, #2980b9); color: white; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; }
                .header h3 { margin: 0; font-size: 1.2rem; }
                .close { background: none; border: none; color: white; font-size: 24px; cursor: pointer; transition: transform 0.2s; }
                .close:hover { transform: scale(1.1); }
                .body { padding: 20px; max-height: 60vh; overflow-y: auto; }
                .footer { padding: 15px 20px; border-top: 1px solid #eee; display: flex; justify-content: flex-end; gap: 10px; }
            </style>
            <div class="overlay" id="overlay">
                <div class="modal">
                    <div class="header"><h3>${this.title}</h3><button class="close" id="closeBtn">&times;</button></div>
                    <div class="body"><slot></slot></div>
                    <div class="footer"><custom-button id="cancelBtn" variant="secondary" size="sm">Cancelar</custom-button><custom-button id="confirmBtn" variant="primary" size="sm">Confirmar</custom-button></div>
                </div>
            </div>
        `;
        this.setupEvents();
    }
    
    setupEvents() {
        const overlay = this.shadowRoot.getElementById('overlay');
        const closeBtn = this.shadowRoot.getElementById('closeBtn');
        const cancelBtn = this.shadowRoot.getElementById('cancelBtn');
        const confirmBtn = this.shadowRoot.getElementById('confirmBtn');
        const closeModal = () => this.close();
        closeBtn?.addEventListener('click', closeModal);
        cancelBtn?.addEventListener('click', closeModal);
        overlay?.addEventListener('click', (e) => { if (e.target === overlay) this.close(); });
        confirmBtn?.addEventListener('click', () => { this.dispatchEvent(new CustomEvent('confirm')); this.close(); });
    }
    
    open() { const overlay = this.shadowRoot.getElementById('overlay'); if(overlay) { overlay.classList.add('open'); this.isOpen = true; this.dispatchEvent(new CustomEvent('open')); } }
    close() { const overlay = this.shadowRoot.getElementById('overlay'); if(overlay) { overlay.classList.remove('open'); this.isOpen = false; this.dispatchEvent(new CustomEvent('close')); } }
    toggle() { this.isOpen ? this.close() : this.open(); }
}
customElements.define('custom-modal', CustomModal);