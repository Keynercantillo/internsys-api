// ============================================
// INTERNSYS - SERVICIO DE OFERTAS
// ============================================

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Función genérica para peticiones HTTP
async function offerRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data && (method === 'POST' || method === 'PUT')) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en la petición');
        }
        
        return await response.json();
    } catch (error) {
        console.error('OfferService Error:', error);
        throw error;
    }
}

// ============================================
// SERVICIO DE OFERTAS
// ============================================
const OfferService = {
    // ============================================
    // OBTENER TODAS LAS OFERTAS
    // ============================================
    getAll: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/get_offers`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Error al obtener ofertas');
            return data;
        } catch (error) {
            console.error('Error en OfferService.getAll:', error);
            throw error;
        }
    },
    
    // ============================================
    // OBTENER OFERTA POR ID
    // ============================================
    getById: async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/get_offer/${id}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Error al obtener oferta');
            return data;
        } catch (error) {
            console.error(`Error en OfferService.getById(${id}):`, error);
            throw error;
        }
    },
    
    // ============================================
    // OBTENER OFERTAS POR EMPRESA
    // ============================================
    getByCompany: async (companyId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/get_offers_by_company/${companyId}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Error al obtener ofertas por empresa');
            return data;
        } catch (error) {
            console.error(`Error en OfferService.getByCompany(${companyId}):`, error);
            throw error;
        }
    },
    
    // ============================================
    // OBTENER OFERTAS DISPONIBLES (para estudiantes)
    // ============================================
    getAvailable: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/get_available_offers`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Error al obtener ofertas disponibles');
            return data;
        } catch (error) {
            console.error('Error en OfferService.getAvailable:', error);
            throw error;
        }
    },
    
    // ============================================
    // CREAR OFERTA
    // ============================================
    create: async (offerData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/create_offer`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(offerData)
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Error al crear oferta');
            return data;
        } catch (error) {
            console.error('Error en OfferService.create:', error);
            throw error;
        }
    },
    
    // ============================================
    // ACTUALIZAR OFERTA
    // ============================================
    update: async (id, offerData) => {
        try {
            const response = await fetch(`${API_BASE_URL}/update_offer/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(offerData)
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Error al actualizar oferta');
            return data;
        } catch (error) {
            console.error(`Error en OfferService.update(${id}):`, error);
            throw error;
        }
    },
    
    // ============================================
    // ELIMINAR OFERTA
    // ============================================
    delete: async (id) => {
        try {
            const response = await fetch(`${API_BASE_URL}/delete_offer/${id}`, {
                method: 'DELETE'
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Error al eliminar oferta');
            return data;
        } catch (error) {
            console.error(`Error en OfferService.delete(${id}):`, error);
            throw error;
        }
    }
};

// ============================================
// EXPOSICIÓN GLOBAL
// ============================================
window.OfferService = OfferService;

console.log("=".repeat(50));
console.log("✅ OfferService Cargado Correctamente");
console.log("✅ OfferService.getAll:", typeof OfferService.getAll === 'function');
console.log("✅ OfferService.getById:", typeof OfferService.getById === 'function');
console.log("✅ OfferService.create:", typeof OfferService.create === 'function');
console.log("✅ OfferService.update:", typeof OfferService.update === 'function');
console.log("✅ OfferService.delete:", typeof OfferService.delete === 'function');
console.log("=".repeat(50));