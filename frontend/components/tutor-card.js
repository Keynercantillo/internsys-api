// components/tutor-card.js
class TutorCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    
    connectedCallback() {
        const id = this.getAttribute('data-id') || '';
        const nombre = this.getAttribute('data-nombre') || 'Tutor';
        const apellido = this.getAttribute('data-apellido') || '';
        const tipo = this.getAttribute('data-tipo') || 'academico';
        const especialidad = this.getAttribute('data-especialidad') || 'No especificada';
        const telefono = this.getAttribute('data-telefono') || 'N/A';
        const email = this.getAttribute('data-email') || 'N/A';
        
        const tipoColor = tipo === 'empresarial' ? '#f39c12' : '#3498db';
        const tipoIcon = tipo === 'empresarial' ? '🏢' : '🏫';
        const nombreCompleto = `${nombre} ${apellido}`;
        
        this.shadowRoot.innerHTML = `
            <style>
                .card { background: white; border-radius: 12px; padding: 16px; margin: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; border-left: 4px solid ${tipoColor}; font-family: 'Segoe UI', sans-serif; }
                .card:hover { transform: translateY(-3px); }
                h3 { margin: 0 0 10px 0; color: #2c3e50; }
                .badge { display: inline-block; background: ${tipoColor}; color: white; padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; margin-bottom: 10px; }
                .row { display: flex; gap: 10px; margin: 8px 0; font-size: 0.9rem; }
                .label { font-weight: bold; width: 85px; color: #555; }
                .tipo { color: ${tipoColor}; font-weight: bold; }
                slot { display: block; margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; }
            </style>
            <div class="card">
                <span class="badge">ID: ${id || 'Nuevo'}</span>
                <h3>${tipoIcon} ${nombreCompleto}</h3>
                <div class="row"><span class="label">📌 Tipo:</span> <span class="tipo">${tipo}</span></div>
                <div class="row"><span class="label">🎓 Especialidad:</span> ${especialidad}</div>
                <div class="row"><span class="label">📞 Teléfono:</span> ${telefono}</div>
                <div class="row"><span class="label">✉️ Email:</span> ${email}</div>
                <slot></slot>
            </div>
        `;
    }
}
customElements.define('tutor-card', TutorCard);