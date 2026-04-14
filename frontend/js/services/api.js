// ============================================
// INTERNSYS - SERVICIOS API
// ============================================

const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Función genérica para peticiones HTTP
async function apiRequest(endpoint, method = 'GET', data = null) {
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
        console.error('API Error:', error);
        throw error;
    }
}

// ============================================
// SERVICIO DE ASIGNACIONES
// ============================================
const AssignmentService = {
    getAll: () => apiRequest('/get_assignments/'),
    getById: (id) => apiRequest(`/get_assignment/${id}`),
    create: (data) => apiRequest('/create_assignment', 'POST', data),
    update: (id, data) => apiRequest(`/update_assignment/${id}`, 'PUT', data),
    delete: (id) => apiRequest(`/delete_assignment/${id}`, 'DELETE'),
    getByStudent: (studentId) => apiRequest(`/get_assignments_by_student/${studentId}`)
};

// ============================================
// SERVICIO DE EVALUACIONES
// ============================================
const EvaluationService = {
    getAll: () => apiRequest('/get_evaluations/'),
    getById: (id) => apiRequest(`/get_evaluation/${id}`),
    create: (data) => apiRequest('/create_evaluation', 'POST', data),
    update: (id, data) => apiRequest(`/update_evaluation/${id}`, 'PUT', data),
    delete: (id) => apiRequest(`/delete_evaluation/${id}`, 'DELETE'),
    getByStudent: (studentId) => apiRequest(`/get_evaluations_by_student/${studentId}`)
};

// ============================================
// SERVICIO DE OFERTAS
// ============================================
const OfferService = {
    getAll: () => apiRequest('/get_offers/'),
    getById: (id) => apiRequest(`/get_offer/${id}`),
    create: (data) => apiRequest('/create_offer', 'POST', data),
    update: (id, data) => apiRequest(`/update_offer/${id}`, 'PUT', data),
    delete: (id) => apiRequest(`/delete_offer/${id}`, 'DELETE'),
    getByCompany: (companyId) => apiRequest(`/get_offers_by_company/${companyId}`)
};

// ============================================
// SERVICIO DE ESTUDIANTES
// ============================================
const StudentService = {
    getAll: () => apiRequest('/get_students/'),
    getById: (id) => apiRequest(`/get_student/${id}`),
    create: (data) => apiRequest('/create_student', 'POST', data),
    update: (id, data) => apiRequest(`/update_student/${id}`, 'PUT', data),
    delete: (id) => apiRequest(`/delete_student/${id}`, 'DELETE')
};

// ============================================
// SERVICIO DE EMPRESAS
// ============================================
const CompanyService = {
    getAll: () => apiRequest('/get_companies/'),
    getById: (id) => apiRequest(`/get_company/${id}`),
    create: (data) => apiRequest('/create_company', 'POST', data),
    update: (id, data) => apiRequest(`/update_company/${id}`, 'PUT', data),
    delete: (id) => apiRequest(`/delete_company/${id}`, 'DELETE')
};

// ============================================
// SERVICIO DE TUTORES
// ============================================
const TutorService = {
    getAll: () => apiRequest('/get_tutors/'),
    getById: (id) => apiRequest(`/get_tutor/${id}`),
    create: (data) => apiRequest('/create_tutor', 'POST', data),
    update: (id, data) => apiRequest(`/update_tutor/${id}`, 'PUT', data),
    delete: (id) => apiRequest(`/delete_tutor/${id}`, 'DELETE')
};

// ============================================
// SERVICIO DE USUARIOS
// ============================================
const UserService = {
    getAll: () => apiRequest('/get_users/'),
    getById: (id) => apiRequest(`/get_user/${id}`),
    create: (data) => apiRequest('/create_user', 'POST', data),
    update: (id, data) => apiRequest(`/update_user/${id}`, 'PUT', data),
    delete: (id) => apiRequest(`/delete_user/${id}`, 'DELETE'),
    login: (email, password) => apiRequest('/login', 'POST', { email, password })
};

// ============================================
// EXPOSICIÓN GLOBAL (para usar en el HTML)
// ============================================
window.AssignmentService = AssignmentService;
window.EvaluationService = EvaluationService;
window.OfferService = OfferService;
window.StudentService = StudentService;
window.CompanyService = CompanyService;
window.TutorService = TutorService;
window.UserService = UserService;

// Mensaje de confirmación
console.log("=".repeat(50));
console.log("✅ API Services Cargados Correctamente");
console.log("✅ AssignmentService:", typeof AssignmentService);
console.log("✅ EvaluationService:", typeof EvaluationService);
console.log("✅ OfferService:", typeof OfferService);
console.log("=".repeat(50));    