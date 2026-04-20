// components/dashboard-stats.js
class DashboardStats extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
    }
    
    connectedCallback() {
        this.render();
        this.loadStats();
    }
    
    render() {
        this.shadowRoot.innerHTML = `
            <style>
                .stats-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; font-family: 'Segoe UI', sans-serif; }
                .stat-card { background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1); transition: transform 0.2s; cursor: pointer; }
                .stat-card:hover { transform: translateY(-5px); box-shadow: 0 4px 16px rgba(0,0,0,0.15); }
                .stat-icon { font-size: 40px; margin-bottom: 10px; }
                .stat-value { font-size: 32px; font-weight: bold; color: #2c3e50; }
                .stat-label { color: #7f8c8d; margin-top: 5px; }
                .loading { text-align: center; padding: 20px; color: #999; }
            </style>
            <div class="stats-container" id="statsContainer"><div class="loading">Cargando estadísticas...</div></div>
        `;
    }
    
    async loadStats() {
        const stats = [
            { icon: "👨‍🎓", label: "Estudiantes", value: 0, link: "students.html" },
            { icon: "🏢", label: "Empresas", value: 0, link: "companies.html" },
            { icon: "📚", label: "Tutores", value: 0, link: "tutors.html" },
            { icon: "💼", label: "Ofertas", value: 0, link: "offers.html" }
        ];
        try {
            const baseUrl = window.location.origin;
            const [students, companies, tutors, offers] = await Promise.all([
                fetch(`${baseUrl}/api/get_students/`).then(r => r.json()),
                fetch(`${baseUrl}/api/get_companies/`).then(r => r.json()),
                fetch(`${baseUrl}/api/get_tutors/`).then(r => r.json()),
                fetch(`${baseUrl}/api/get_offers/`).then(r => r.json())
            ]);
            stats[0].value = students.result?.length || 0;
            stats[1].value = companies.result?.length || 0;
            stats[2].value = tutors.result?.length || 0;
            stats[3].value = offers.result?.length || 0;
        } catch(e) { console.error(e); stats.forEach(s => s.value = '?'); }
        const container = this.shadowRoot.getElementById('statsContainer');
        container.innerHTML = stats.map(s => `<div class="stat-card" data-link="${s.link}"><div class="stat-icon">${s.icon}</div><div class="stat-value">${s.value}</div><div class="stat-label">${s.label}</div></div>`).join('');
        container.querySelectorAll('.stat-card').forEach(card => { card.addEventListener('click', () => { window.location.href = card.dataset.link; }); });
    }
}
customElements.define('dashboard-stats', DashboardStats);