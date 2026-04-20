// components/offer-card.js
class OfferCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    
    connectedCallback() {
        const id = this.getAttribute('data-id') || '';
        const title = this.getAttribute('data-title') || 'Oferta';
        const company = this.getAttribute('data-company') || 'Empresa';
        const vacancies = this.getAttribute('data-vacancies') || '0';
        const startDate = this.getAttribute('data-start-date') || 'No definida';
        const status = this.getAttribute('data-status') || 'disponible';
        
        const statusColor = status === 'disponible' ? '#27ae60' : '#e74c3c';
        const statusText = status === 'disponible' ? 'Disponible' : 'Ocupado';
        
        this.shadowRoot.innerHTML = `
            <style>
                .card { background: white; border-radius: 12px; padding: 16px; margin: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; border-left: 4px solid #f39c12; font-family: 'Segoe UI', sans-serif; }
                .card:hover { transform: translateY(-3px); }
                h3 { margin: 0 0 10px 0; color: #2c3e50; }
                .badge { display: inline-block; background: #f39c12; color: white; padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; margin-right: 8px; }
                .vacancies-badge { display: inline-block; background: #3498db; color: white; padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; }
                .row { display: flex; gap: 10px; margin: 8px 0; font-size: 0.9rem; }
                .label { font-weight: bold; width: 80px; color: #555; }
                .status { color: ${statusColor}; font-weight: bold; }
                slot { display: block; margin-top: 12px; padding-top: 12px; border-top: 1px solid #eee; }
            </style>
            <div class="card">
                <div><span class="badge">ID: ${id || 'Nuevo'}</span><span class="vacancies-badge">📊 ${vacancies} vacantes</span></div>
                <h3>💼 ${title}</h3>
                <div class="row"><span class="label">🏢 Empresa:</span> ${company}</div>
                <div class="row"><span class="label">📅 Inicio:</span> ${startDate}</div>
                <div class="row"><span class="label">📌 Estado:</span> <span class="status">${statusText}</span></div>
                <slot></slot>
            </div>
        `;
    }
}
customElements.define('offer-card', OfferCard);