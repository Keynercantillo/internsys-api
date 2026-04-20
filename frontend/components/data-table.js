// components/data-table.js
class DataTable extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.data = [];
        this.columns = [];
        this.currentPage = 1;
        this.rowsPerPage = 10;
        this.searchTerm = '';
    }
    
    connectedCallback() {
        this.title = this.getAttribute('title') || 'Tabla de Datos';
        this.render();
    }
    
    render() {
        this.shadowRoot.innerHTML = `
            <style>
                .table-container { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); font-family: 'Segoe UI', sans-serif; }
                .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px; }
                .header h3 { margin: 0; color: #2c3e50; }
                .search-input { padding: 8px 12px; border: 1px solid #ddd; border-radius: 8px; width: 250px; font-size: 14px; }
                table { width: 100%; border-collapse: collapse; }
                th { background: #3498db; color: white; padding: 12px; text-align: left; font-weight: 600; }
                td { padding: 10px 12px; border-bottom: 1px solid #eee; }
                tr:hover { background: #f8f9fa; }
                .pagination { display: flex; justify-content: flex-end; gap: 8px; margin-top: 20px; }
                .page-btn { padding: 6px 12px; border: 1px solid #ddd; background: white; border-radius: 5px; cursor: pointer; transition: all 0.2s; }
                .page-btn:hover { background: #3498db; color: white; }
                .page-btn.active { background: #3498db; color: white; }
                .empty { text-align: center; padding: 40px; color: #999; }
            </style>
            <div class="table-container">
                <div class="header"><h3>${this.title}</h3><input type="text" class="search-input" id="searchInput" placeholder="🔍 Buscar..."></div>
                <div id="tableBody"></div><div class="pagination" id="pagination"></div>
            </div>
        `;
        this.shadowRoot.getElementById('searchInput')?.addEventListener('input', (e) => {
            this.searchTerm = e.target.value.toLowerCase();
            this.currentPage = 1;
            this.renderTable();
        });
    }
    
    setData(columns, data) { this.columns = columns; this.data = data; this.allData = [...data]; this.renderTable(); }
    
    renderTable() {
        const container = this.shadowRoot.getElementById('tableBody');
        if (!container) return;
        let filteredData = this.allData || [];
        if (this.searchTerm) filteredData = this.allData.filter(row => Object.values(row).some(value => String(value).toLowerCase().includes(this.searchTerm)));
        const totalPages = Math.ceil(filteredData.length / this.rowsPerPage);
        const start = (this.currentPage - 1) * this.rowsPerPage;
        const paginatedData = filteredData.slice(start, start + this.rowsPerPage);
        if (!paginatedData.length) { container.innerHTML = '<div class="empty">No hay datos disponibles</div>'; this.renderPagination(totalPages); return; }
        let html = '<div style="overflow-x: auto;"><table><thead><tr>';
        this.columns.forEach(col => html += `<th>${col.title}</th>`);
        html += '</thead><tbody>';
        paginatedData.forEach(row => {
            html += '<tr>';
            this.columns.forEach(col => { let value = row[col.key]; if (value === undefined || value === null) value = '-'; html += `<td>${value}</td>`; });
            html += '</tr>';
        });
        html += '</tbody></table></div>';
        container.innerHTML = html;
        this.renderPagination(totalPages);
    }
    
    renderPagination(totalPages) {
        const paginationDiv = this.shadowRoot.getElementById('pagination');
        if (!paginationDiv || totalPages <= 1) { if (paginationDiv) paginationDiv.innerHTML = ''; return; }
        let html = '';
        for (let i = 1; i <= totalPages; i++) html += `<button class="page-btn ${i === this.currentPage ? 'active' : ''}" data-page="${i}">${i}</button>`;
        paginationDiv.innerHTML = html;
        paginationDiv.querySelectorAll('.page-btn').forEach(btn => { btn.addEventListener('click', () => { this.currentPage = parseInt(btn.dataset.page); this.renderTable(); }); });
    }
    
    refresh(data) { if (data) this.allData = data; this.currentPage = 1; this.searchTerm = ''; const searchInput = this.shadowRoot.getElementById('searchInput'); if (searchInput) searchInput.value = ''; this.renderTable(); }
}
customElements.define('data-table', DataTable);