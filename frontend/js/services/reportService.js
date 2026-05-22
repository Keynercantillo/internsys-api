// js/services/reportService.js
// Servicio para conectar con la API de reportes en FastAPI

const API_BASE_URL = 'http://localhost:8000'; // Cambia por tu URL

const ReportService = {
    
    // ============================================
    // Crear un nuevo reporte
    // ============================================
    async create(reportData) {
        try {
            const response = await fetch(`${API_BASE_URL}/create_report`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reportData)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al crear el reporte');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error en ReportService.create:', error);
            throw error;
        }
    },
    
    // ============================================
    // Obtener un reporte por ID
    // ============================================
    async getById(reportId) {
        try {
            const response = await fetch(`${API_BASE_URL}/get_report/${reportId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al obtener el reporte');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error en ReportService.getById:', error);
            throw error;
        }
    },
    
    // ============================================
    // Obtener todos los reportes
    // ============================================
    async getAll() {
        try {
            const response = await fetch(`${API_BASE_URL}/get_reports/`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al obtener los reportes');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error en ReportService.getAll:', error);
            throw error;
        }
    },
    
    // ============================================
    // Obtener reportes por tipo
    // ============================================
    async getByType(reportType) {
        try {
            const response = await fetch(`${API_BASE_URL}/get_reports_by_type/${reportType}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al obtener los reportes por tipo');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error en ReportService.getByType:', error);
            throw error;
        }
    },
    
    // ============================================
    // Actualizar un reporte
    // ============================================
    async update(reportId, reportData) {
        try {
            const response = await fetch(`${API_BASE_URL}/update_report/${reportId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(reportData)
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al actualizar el reporte');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error en ReportService.update:', error);
            throw error;
        }
    },
    
    // ============================================
    // Eliminar un reporte
    // ============================================
    async delete(reportId) {
        try {
            const response = await fetch(`${API_BASE_URL}/delete_report/${reportId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Error al eliminar el reporte');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error en ReportService.delete:', error);
            throw error;
        }
    }
};

// Exportar para usar en otros archivos
window.ReportService = ReportService;