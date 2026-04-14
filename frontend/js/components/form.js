// ============================================
// COMPONENTE FORMULARIOS
// ============================================

class FormComponent {
    constructor(formId, options = {}) {
        this.formId = formId;
        this.form = document.getElementById(formId);
        this.options = {
            validateOnSubmit: true,
            resetOnSuccess: false,
            ...options
        };
        this.fields = {};
        this.init();
    }
    
    // Inicializar
    init() {
        if (!this.form) return;
        
        // Recopilar campos
        this.form.querySelectorAll('input, select, textarea').forEach(field => {
            if (field.name) {
                this.fields[field.name] = field;
            }
        });
        
        // Configurar submit
        if (this.options.validateOnSubmit) {
            this.form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.validateAndSubmit();
            });
        }
    }
    
    // Validar campo
    validateField(field) {
        const value = field.value.trim();
        const rules = field.dataset.rules ? field.dataset.rules.split('|') : [];
        
        for (const rule of rules) {
            const [ruleName, ruleValue] = rule.split(':');
            
            switch (ruleName) {
                case 'required':
                    if (!value) {
                        this.showError(field, 'Este campo es requerido');
                        return false;
                    }
                    break;
                case 'email':
                    if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                        this.showError(field, 'Ingrese un email válido');
                        return false;
                    }
                    break;
                case 'min':
                    if (value.length < parseInt(ruleValue)) {
                        this.showError(field, `Mínimo ${ruleValue} caracteres`);
                        return false;
                    }
                    break;
                case 'max':
                    if (value.length > parseInt(ruleValue)) {
                        this.showError(field, `Máximo ${ruleValue} caracteres`);
                        return false;
                    }
                    break;
                case 'number':
                    if (value && isNaN(value)) {
                        this.showError(field, 'Ingrese un número válido');
                        return false;
                    }
                    break;
            }
        }
        
        this.clearError(field);
        return true;
    }
    
    // Validar todos los campos
    validateAll() {
        let isValid = true;
        for (const [name, field] of Object.entries(this.fields)) {
            if (!this.validateField(field)) {
                isValid = false;
            }
        }
        return isValid;
    }
    
    // Mostrar error
    showError(field, message) {
        field.classList.add('is-invalid');
        
        let errorDiv = field.parentElement.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentElement.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }
    
    // Limpiar error
    clearError(field) {
        field.classList.remove('is-invalid');
        const errorDiv = field.parentElement.querySelector('.invalid-feedback');
        if (errorDiv) {
            errorDiv.remove();
        }
    }
    
    // Obtener datos del formulario
    getData() {
        const data = {};
        for (const [name, field] of Object.entries(this.fields)) {
            data[name] = field.type === 'checkbox' ? field.checked : field.value;
        }
        return data;
    }
    
    // Rellenar formulario
    setData(data) {
        for (const [name, value] of Object.entries(data)) {
            if (this.fields[name]) {
                if (this.fields[name].type === 'checkbox') {
                    this.fields[name].checked = value;
                } else {
                    this.fields[name].value = value;
                }
            }
        }
    }
    
    // Limpiar formulario
    reset() {
        this.form.reset();
        for (const field of Object.values(this.fields)) {
            this.clearError(field);
        }
    }
    
    // Validar y enviar
    async validateAndSubmit(onSuccess, onError) {
        if (this.validateAll()) {
            try {
                const data = this.getData();
                if (onSuccess) {
                    await onSuccess(data);
                }
                if (this.options.resetOnSuccess) {
                    this.reset();
                }
            } catch (error) {
                if (onError) {
                    onError(error);
                }
                if (typeof AlertComponent !== 'undefined') {
                    AlertComponent.error(error.message);
                }
            }
        }
    }
    
    // Deshabilitar formulario
    disable(disabled = true) {
        for (const field of Object.values(this.fields)) {
            field.disabled = disabled;
        }
    }
}

// Función helper para crear formulario rápidamente
function createForm(formId, fields, onSubmit) {
    const form = document.getElementById(formId);
    if (!form) return null;
    
    const formComponent = new FormComponent(formId);
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (formComponent.validateAll()) {
            const data = formComponent.getData();
            await onSubmit(data);
        }
    });
    
    return formComponent;
}