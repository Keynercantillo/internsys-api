// components/student-card.js
class StudentCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    
    connectedCallback() {
        const id = this.getAttribute('data-id') || '';
        const nombre = this.getAttribute('data-nombre') || 'Estudiante';
        const apellido = this.getAttribute('data-apellido') || '';
        const cedula = this.getAttribute('data-cedula') || 'N/A';
        const edad = this.getAttribute('data-edad') || 'N/A';
        const carrera = this.getAttribute('data-carrera') || 'N/A';
        const semestre = this.getAttribute('data-semestre') || 'N/A';
        const promedio = this.getAttribute('data-promedio') || '0';
        
        const nombreCompleto = `${nombre} ${apellido}`;
        let promedioColor = promedio >= 4 ? '#27ae60' : (promedio >= 3 ? '#f39c12' : '#e74c3c');
        let promedioIcon = promedio >= 4 ? '⭐' : (promedio >= 3 ? '📘' : '⚠️');
        
        this.shadowRoot.innerHTML = `
            <style>
                .card { background: white; border-radius: 12px; padding: 16px; margin: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; border-left: 4px solid #3498db; font-family: 'Segoe UI', sans-serif; }
                .card:hover { transform: translateY(-3px); }
                h3 { margin: 0 0 10px 0; color: #2c3e50; font-size: 1.1rem; }
                .badge { display: inline-block; background: #3498db; color: white; padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; margin-bottom: 10px; }
                .row { display: flex; gap: 10px; margin: 8px 0; font-size: 0.9rem; }
                .label { font-weight: bold; width: 75px; color: #555; }
                .promedio { color: ${promedioColor}; font-weight: bold; }
                slot { display: block; margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; }
            </style>
            <div class="card">
                <span class="badge">ID: ${id || 'Nuevo'}</span>
                <h3>${nombreCompleto}</h3>
                <div class="row"><span class="label">📄 Cédula:</span> ${cedula}</div>
                <div class="row"><span class="label">🎂 Edad:</span> ${edad} años</div>
                <div class="row"><span class="label">📚 Carrera:</span> ${carrera}</div>
                <div class="row"><span class="label">📖 Semestre:</span> ${semestre}</div>
                <div class="row"><span class="label">⭐ Promedio:</span> <span class="promedio">${promedioIcon} ${promedio}</span></div>
                <slot></slot>
            </div>
        `;
    }
}
customElements.define('student-card', StudentCard);