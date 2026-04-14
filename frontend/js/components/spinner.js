// ============================================
// COMPONENTE SPINNER / CARGA
// ============================================

class SpinnerComponent {
    constructor() {
        this.spinner = null;
    }
    
    // Mostrar spinner global
    show(message = 'Cargando...') {
        // Eliminar spinner existente
        this.hide();
        
        // Crear spinner
        this.spinner = document.createElement('div');
        this.spinner.className = 'spinner-overlay';
        this.spinner.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">${message}</span>
                </div>
                <div class="mt-2 text-white">${message}</div>
            </div>
        `;
        
        document.body.appendChild(this.spinner);
    }
    
    // Ocultar spinner
    hide() {
        if (this.spinner) {
            this.spinner.remove();
            this.spinner = null;
        }
    }
    
    // Mostrar spinner en elemento específico
    showInElement(elementId, message = 'Cargando...') {
        const element = document.getElementById(elementId);
        if (element) {
            const originalContent = element.innerHTML;
            element.innerHTML = `
                <div class="text-center p-5">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">${message}</span>
                    </div>
                    <p class="mt-2">${message}</p>
                </div>
            `;
            element.dataset.originalContent = originalContent;
        }
    }
    
    // Ocultar spinner en elemento específico
    hideInElement(elementId) {
        const element = document.getElementById(elementId);
        if (element && element.dataset.originalContent) {
            element.innerHTML = element.dataset.originalContent;
            delete element.dataset.originalContent;
        }
    }
    
    // Mostrar spinner en botón
    showOnButton(buttonId, text = 'Procesando...') {
        const button = document.getElementById(buttonId);
        if (button) {
            button.dataset.originalText = button.innerHTML;
            button.disabled = true;
            button.innerHTML = `<span class="spinner-border spinner-border-sm me-2"></span> ${text}`;
        }
    }
    
    // Ocultar spinner en botón
    hideOnButton(buttonId) {
        const button = document.getElementById(buttonId);
        if (button && button.dataset.originalText) {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText;
            delete button.dataset.originalText;
        }
    }
}

// Instancia global
const Spinner = new SpinnerComponent();

// Función para ejecutar con spinner
async function withSpinner(asyncFunction, message = 'Procesando...') {
    Spinner.show(message);
    try {
        const result = await asyncFunction();
        Spinner.hide();
        return result;
    } catch (error) {
        Spinner.hide();
        throw error;
    }
}