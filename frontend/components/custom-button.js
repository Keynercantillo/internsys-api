// components/custom-button.js
class CustomButton extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    
    connectedCallback() {
        const variant = this.getAttribute('variant') || 'primary';
        const size = this.getAttribute('size') || 'md';
        const disabled = this.hasAttribute('disabled');
        const fullWidth = this.hasAttribute('full-width');
        
        const variants = {
            primary: 'background: linear-gradient(135deg, #3498db, #2980b9); color: white;',
            success: 'background: linear-gradient(135deg, #27ae60, #229954); color: white;',
            danger: 'background: linear-gradient(135deg, #e74c3c, #c0392b); color: white;',
            warning: 'background: linear-gradient(135deg, #f39c12, #e67e22); color: white;',
            secondary: 'background: #95a5a6; color: white;',
            outline: 'background: transparent; border: 2px solid #3498db; color: #3498db;'
        };
        
        const sizes = {
            sm: 'padding: 6px 12px; font-size: 12px;',
            md: 'padding: 10px 20px; font-size: 14px;',
            lg: 'padding: 14px 28px; font-size: 16px;'
        };
        
        const width = fullWidth ? 'width: 100%;' : '';
        
        this.shadowRoot.innerHTML = `
            <style>
                button {
                    ${variants[variant]}
                    ${sizes[size]}
                    ${width}
                    border: none;
                    border-radius: 8px;
                    cursor: ${disabled ? 'not-allowed' : 'pointer'};
                    font-weight: 600;
                    font-family: 'Segoe UI', sans-serif;
                    transition: all 0.3s ease;
                    opacity: ${disabled ? '0.6' : '1'};
                }
                button:hover { transform: ${disabled ? 'none' : 'translateY(-2px)'}; box-shadow: ${disabled ? 'none' : '0 4px 12px rgba(0,0,0,0.2)'}; }
                button:active { transform: ${disabled ? 'none' : 'translateY(0)'}; }
            </style>
            <button ${disabled ? 'disabled' : ''}>
                <slot></slot>
            </button>
        `;
        
        if (!disabled) {
            this.shadowRoot.querySelector('button').addEventListener('click', (e) => {
                this.dispatchEvent(new CustomEvent('click', { bubbles: true, detail: e }));
            });
        }
    }
}
customElements.define('custom-button', CustomButton);