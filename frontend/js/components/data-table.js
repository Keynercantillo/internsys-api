// ============================================
// COMPONENTE DATATABLE
// ============================================

class DataTableComponent {
    constructor(tableId, options = {}) {
        this.tableId = tableId;
        this.table = null;
        this.options = {
            pageLength: 10,
            lengthMenu: [[5, 10, 25, 50, -1], [5, 10, 25, 50, "Todos"]],
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
            },
            responsive: true,
            ordering: true,
            searching: true,
            paging: true,
            info: true,
            ...options
        };
    }
    
    // Inicializar tabla
    init(data, columns, hasActions = false) {
        const tableElement = $(`#${this.tableId}`);
        
        if (this.table) {
            this.table.destroy();
        }
        
        // Limpiar tabla
        tableElement.find('tbody').empty();
        
        // Configurar columnas
        const thead = tableElement.find('thead');
        thead.empty();
        let theadRow = $('<tr></tr>');
        
        columns.forEach(col => {
            theadRow.append(`<th>${col.title}</th>`);
        });
        
        if (hasActions) {
            theadRow.append('<th>Acciones</th>');
        }
        
        thead.append(theadRow);
        
        // Configurar datos
        const formattedData = data.map(row => {
            const formattedRow = [...row];
            if (hasActions) {
                formattedRow.push(row.actions || '');
            }
            return formattedRow;
        });
        
        // Inicializar DataTable
        this.table = tableElement.DataTable({
            data: formattedData,
            columns: columns.map(col => ({ data: col.data || null, title: col.title })),
            ...this.options
        });
        
        return this.table;
    }
    
    // Refrescar datos
    refresh(data) {
        if (this.table) {
            this.table.clear();
            this.table.rows.add(data);
            this.table.draw();
        }
    }
    
    // Agregar fila
    addRow(data) {
        if (this.table) {
            this.table.row.add(data).draw();
        }
    }
    
    // Eliminar fila
    deleteRow(index) {
        if (this.table) {
            this.table.row(index).remove().draw();
        }
    }
    
    // Obtener todas las filas
    getData() {
        return this.table ? this.table.rows().data().toArray() : [];
    }
    
    // Destruir tabla
    destroy() {
        if (this.table) {
            this.table.destroy();
            this.table = null;
        }
    }
    
    // Buscar
    search(value) {
        if (this.table) {
            this.table.search(value).draw();
        }
    }
    
    // Ordenar
    order(column, direction = 'asc') {
        if (this.table) {
            this.table.order([column, direction]).draw();
        }
    }
}

// Función helper para crear DataTable rápidamente
function createDataTable(tableId, data, columns, options = {}) {
    const dt = new DataTableComponent(tableId, options);
    dt.init(data, columns);
    return dt;
}