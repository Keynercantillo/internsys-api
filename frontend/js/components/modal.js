// ============================================
// COMPONENTE MODAL
// ============================================

class ModalComponent {
    constructor(modalId, options = {}) {
        this.modalId = modalId;
        this.modal = null;
        this.options = {
            backdrop: true,
            keyboard: true,
            focus: true,
            ...options
        };
    }
    
    // Inicializar modal
    init() {
        const modalElement = document.getElementById(this.modalId);
        if (modalElement) {
            this.modal = new bootstrap.Modal(modalElement, this.options);
        }
        return this.modal;
    }
    
    // Abrir modal
    open() {
        if (this.modal) {
            this.modal.show();
        } else {
            this.init();
            this.modal.show();
        }
    }
    
    // Cerrar modal
    close() {
        if (this.modal) {
            this.modal.hide();
        }
    }
    
    // Alternar modal
    toggle() {
        if (this.modal) {
            this.modal.toggle();
        }
    }
    
    // Establecer título
    setTitle(title) {
        const titleElement = document.querySelector(`#${this.modalId} .modal-title`);
        if (titleElement) {
            titleElement.innerHTML = title;
        }
    }
    
    // Establecer contenido del body
    setBody(content) {
        const bodyElement = document.querySelector(`#${this.modalId} .modal-body`);
        if (bodyElement) {
            bodyElement.innerHTML = content;
        }
    }
    
    // Establecer contenido del footer
    setFooter(content) {
        const footerElement = document.querySelector(`#${this.modalId} .modal-footer`);
        if (footerElement) {
            footerElement.innerHTML = content;
        }
    }
    
    // Limpiar modal
    clear() {
        this.setTitle('');
        this.setBody('');
        this.setFooter('');
    }
    
    // Configurar tamaño
    setSize(size) {
        const modalDialog = document.querySelector(`#${this.modalId} .modal-dialog`);
        if (modalDialog) {
            modalDialog.classList.remove('modal-sm', 'modal-lg', 'modal-xl');
            if (size === 'sm') modalDialog.classList.add('modal-sm');
            if (size === 'lg') modalDialog.classList.add('modal-lg');
            if (size === 'xl') modalDialog.classList.add('modal-xl');
        }
    }
    
    // Evento al abrir
    onOpen(callback) {
        const modalElement = document.getElementById(this.modalId);
        if (modalElement) {
            modalElement.addEventListener('show.bs.modal', callback);
        }
    }
    
    // Evento al cerrar
    onClose(callback) {
        const modalElement = document.getElementById(this.modalId);
        if (modalElement) {
            modalElement.addEventListener('hide.bs.modal', callback);
        }
    }
}

// Función helper para crear modal rápidamente
function createModal(modalId, title, body, options = {}) {
    // Crear estructura del modal si no existe
    if (!document.getElementById(modalId)) {
        const modalHtml = `
            <div class="modal fade" id="${modalId}" tabindex="-1">
                <div class="modal-dialog ${options.size === 'lg' ? 'modal-lg' : options.size === 'sm' ? 'modal-sm' : ''}">
                    <div class="modal-content">
                        <div class="modal-header bg-primary text-white">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            ${body}
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-primary" id="modalSaveBtn">Guardar</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
    
    return new ModalComponent(modalId);
}