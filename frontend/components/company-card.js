// components/company-card.js
class CompanyCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    
    connectedCallback() {
        const id = this.getAttribute('data-id') || '';
        const name = this.getAttribute('data-name') || 'Empresa';
        const ruc = this.getAttribute('data-ruc') || 'N/A';
        const sector = this.getAttribute('data-sector') || 'No especificado';
        const phone = this.getAttribute('data-phone') || 'N/A';
        const email = this.getAttribute('data-email') || 'N/A';
        const address = this.getAttribute('data-address') || 'No especificada';
        const status = this.getAttribute('data-status') || 'activo';
        
        const statusColor = status === 'activo' ? '#27ae60' : '#e74c3c';
        const statusText = status === 'activo' ? 'Activo' : 'Inactivo';
        
        this.shadowRoot.innerHTML = `
            <style>
                .card {
                    background: white;
                    border-radius: 12px;
                    padding: 16px;
                    margin: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    transition: transform 0.2s;
                    border-left: 4px solid #27ae60;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }
                .card:hover { transform: translateY(-3px); }
                h3 { margin: 0 0 10px 0; color: #2c3e50; }
                .badge {
                    display: inline-block;
                    background: #27ae60;
                    color: white;
                    padding: 2px 8px;
                    border-radius: 20px;
                    font-size: 0.7rem;
                    margin-bottom: 10px;
                }
                .row { display: flex; gap: 10px; margin: 8px 0; font-size: 0.9rem; }
                .label { font-weight: bold; width: 75px; color: #555; }
                .status { color: ${statusColor}; font-weight: bold; }
                slot {
                    display: block;
                    margin-top: 12px;
                    padding-top: 12px;
                    border-top: 1px solid #eee;
                }
            </style>
            <div class="card">
                <span class="badge">ID: ${id || 'Nuevo'}</span>
                <h3>🏢 ${name}</h3>
                <div class="row"><span class="label">📋 RUC:</span> ${ruc}</div>
                <div class="row"><span class="label">🏭 Sector:</span> ${sector}</div>
                <div class="row"><span class="label">📞 Teléfono:</span> ${phone}</div>
                <div class="row"><span class="label">✉️ Email:</span> ${email}</div>
                <div class="row"><span class="label">📍 Dirección:</span> ${address.substring(0, 50)}${address.length > 50 ? '...' : ''}</div>
                <div class="row"><span class="label">📊 Estado:</span> <span class="status">${statusText}</span></div>
                <slot></slot>
            </div>
        `;
    }
}

customElements.define('company-card', CompanyCard);