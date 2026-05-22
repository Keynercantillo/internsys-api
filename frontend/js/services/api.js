// ============================================
// API SERVICE - InternSys (VERSIÓN COMPLETA)
// ============================================

const API_BASE_URL = 'http://localhost:8000/api';

// Función genérica para peticiones fetch
async function fetchAPI(endpoint, options = {}) {
    const token = localStorage.getItem('internsys_token');
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    const config = {
        ...options,
        headers
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en la petición');
        }
        return await response.json();
    } catch (error) {
        console.error(`Error en ${endpoint}:`, error);
        throw error;
    }
}

// ============================================
// AUTH SERVICE
// ============================================
const AuthService = {
    register: async (userData) => {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(userData)
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Error al registrar');
        return data;
    },
    
    login: async (usuario, contraseña) => {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario, contraseña })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Error al iniciar sesión');
        localStorage.setItem('internsys_user', JSON.stringify(data));
        return data;
    },
    
    logout: () => {
        localStorage.removeItem('internsys_user');
        localStorage.removeItem('internsys_token');
        window.location.href = 'index.html';
    },
    
    getCurrentUser: () => {
        const user = localStorage.getItem('internsys_user');
        return user ? JSON.parse(user) : null;
    },
    
    changePassword: async (userId, oldPassword, newPassword) => {
        return await fetchAPI(`/change_password/${userId}`, {
            method: 'PUT',
            body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
        });
    }
};

// ============================================
// STUDENTS SERVICE
// ============================================
const StudentService = {
    getAll: async () => {
        return await fetchAPI('/get_students/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_student/${id}`);
    },
    getByTutor: async (tutorId) => {
        return await fetchAPI(`/get_students_by_tutor/${tutorId}`);
    },
    getByCompany: async (companyId) => {
        return await fetchAPI(`/get_students_by_company/${companyId}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_student', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_student/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_student/${id}`, {
            method: 'DELETE'
        });
    },
    updateProgress: async (id, hours) => {
        return await fetchAPI(`/update_student_progress/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ completed_hours: hours })
        });
    }
};

// ============================================
// TUTORS SERVICE
// ============================================
const TutorService = {
    getAll: async () => {
        return await fetchAPI('/get_tutors/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_tutor/${id}`);
    },
    getByCompany: async (companyId) => {
        return await fetchAPI(`/get_tutors_by_company/${companyId}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_tutor', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_tutor/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_tutor/${id}`, {
            method: 'DELETE'
        });
    },
    getStudents: async (tutorId) => {
        return await fetchAPI(`/get_tutor_students/${tutorId}`);
    }
};

// ============================================
// COMPANIES SERVICE
// ============================================
const CompanyService = {
    getAll: async () => {
        return await fetchAPI('/get_companies/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_company/${id}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_company', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_company/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_company/${id}`, {
            method: 'DELETE'
        });
    },
    getOffers: async (companyId) => {
        return await fetchAPI(`/get_company_offers/${companyId}`);
    },
    getApplications: async (companyId) => {
        return await fetchAPI(`/get_company_applications/${companyId}`);
    }
};

// ============================================
// OFFERS SERVICE (Ofertas de práctica)
// ============================================
const OfferService = {
    getAll: async () => {
        return await fetchAPI('/get_offers/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_offer/${id}`);
    },
    getByCompany: async (companyId) => {
        return await fetchAPI(`/get_offers_by_company/${companyId}`);
    },
    getActive: async () => {
        return await fetchAPI('/get_active_offers/');
    },
    create: async (data) => {
        return await fetchAPI('/create_offer', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_offer/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_offer/${id}`, {
            method: 'DELETE'
        });
    },
    publish: async (id) => {
        return await fetchAPI(`/publish_offer/${id}`, {
            method: 'PUT'
        });
    },
    close: async (id) => {
        return await fetchAPI(`/close_offer/${id}`, {
            method: 'PUT'
        });
    }
};

// ============================================
// APPLICATIONS SERVICE (Postulaciones)
// ============================================
const ApplicationService = {
    getAll: async () => {
        return await fetchAPI('/get_applications/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_application/${id}`);
    },
    getByCompany: async (companyId) => {
        return await fetchAPI(`/get_applications_by_company/${companyId}`);
    },
    getByOffer: async (offerId) => {
        return await fetchAPI(`/get_applications_by_offer/${offerId}`);
    },
    getByStudent: async (studentId) => {
        return await fetchAPI(`/get_applications_by_student/${studentId}`);
    },
    getPending: async (companyId) => {
        return await fetchAPI(`/get_pending_applications/${companyId}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_application', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    updateStatus: async (applicationId, status, comments = null) => {
        return await fetchAPI(`/update_application_status/${applicationId}`, {
            method: 'PUT',
            body: JSON.stringify({ status, comments })
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_application/${id}`, {
            method: 'DELETE'
        });
    },
    getStats: async (companyId) => {
        return await fetchAPI(`/get_application_stats/${companyId}`);
    },
    bulkUpdate: async (applications) => {
        return await fetchAPI('/bulk_update_applications', {
            method: 'PUT',
            body: JSON.stringify({ applications })
        });
    }
};

// ============================================
// ASSIGNMENTS SERVICE (Asignaciones estudiante-tutor)
// ============================================
const AssignmentService = {
    getAll: async () => {
        return await fetchAPI('/get_assignments/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_assignment/${id}`);
    },
    getByStudent: async (studentId) => {
        return await fetchAPI(`/get_assignments_by_student/${studentId}`);
    },
    getByTutor: async (tutorId) => {
        return await fetchAPI(`/get_assignments_by_tutor/${tutorId}`);
    },
    getByCompany: async (companyId) => {
        return await fetchAPI(`/get_assignments_by_company/${companyId}`);
    },
    getActive: async () => {
        return await fetchAPI('/get_active_assignments/');
    },
    create: async (data) => {
        return await fetchAPI('/create_assignment', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_assignment/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_assignment/${id}`, {
            method: 'DELETE'
        });
    },
    complete: async (id, completedHours) => {
        return await fetchAPI(`/complete_assignment/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ completed_hours: completedHours })
        });
    },
    getProgress: async (studentId) => {
        return await fetchAPI(`/get_assignment_progress/${studentId}`);
    }
};

// ============================================
// EVALUATIONS SERVICE
// ============================================
const EvaluationService = {
    getAll: async () => {
        return await fetchAPI('/get_evaluations/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_evaluation/${id}`);
    },
    getByStudent: async (studentId) => {
        return await fetchAPI(`/get_evaluations_by_student/${studentId}`);
    },
    getByTutor: async (tutorId) => {
        return await fetchAPI(`/get_evaluations_by_tutor/${tutorId}`);
    },
    getByAssignment: async (assignmentId) => {
        return await fetchAPI(`/get_evaluations_by_assignment/${assignmentId}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_evaluation', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_evaluation/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_evaluation/${id}`, {
            method: 'DELETE'
        });
    },
    getAverage: async (studentId) => {
        return await fetchAPI(`/get_student_evaluation_average/${studentId}`);
    },
    getReports: async (evaluationId) => {
        return await fetchAPI(`/get_evaluation_reports/${evaluationId}`);
    }
};

// ============================================
// USERS SERVICE
// ============================================
const UserService = {
    getAll: async () => {
        return await fetchAPI('/get_users/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_user/${id}`);
    },
    getByRole: async (role) => {
        return await fetchAPI(`/get_users_by_role/${role}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_user', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_user/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_user/${id}`, {
            method: 'DELETE'
        });
    },
    activate: async (id) => {
        return await fetchAPI(`/activate_user/${id}`, {
            method: 'PUT'
        });
    },
    deactivate: async (id) => {
        return await fetchAPI(`/deactivate_user/${id}`, {
            method: 'PUT'
        });
    }
};

// ============================================
// REPORTS SERVICE
// ============================================
const ReportService = {
    getAll: async () => {
        return await fetchAPI('/get_reports/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_report/${id}`);
    },
    getByUser: async (userId) => {
        return await fetchAPI(`/get_reports_by_user/${userId}`);
    },
    getByType: async (type) => {
        return await fetchAPI(`/get_reports_by_type/${type}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_report', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_report/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_report/${id}`, {
            method: 'DELETE'
        });
    },
    generatePDF: async (id) => {
        return await fetchAPI(`/generate_report_pdf/${id}`);
    },
    generateExcel: async (id) => {
        return await fetchAPI(`/generate_report_excel/${id}`);
    }
};

// ============================================
// NOTIFICATIONS SERVICE
// ============================================
const NotificationService = {
    getAll: async () => {
        return await fetchAPI('/get_notifications/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_notification/${id}`);
    },
    getByUser: async (userId) => {
        return await fetchAPI(`/get_notifications_by_user/${userId}`);
    },
    getUnread: async (userId) => {
        return await fetchAPI(`/get_unread_notifications/${userId}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_notification', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    markAsRead: async (id) => {
        return await fetchAPI(`/mark_notification_read/${id}`, {
            method: 'PUT'
        });
    },
    markAllAsRead: async (userId) => {
        return await fetchAPI(`/mark_all_notifications_read/${userId}`, {
            method: 'PUT'
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_notification/${id}`, {
            method: 'DELETE'
        });
    },
    sendBulk: async (users, message) => {
        return await fetchAPI('/send_bulk_notifications', {
            method: 'POST',
            body: JSON.stringify({ users, message })
        });
    }
};

// ============================================
// FOLLOWUP VISITS SERVICE
// ============================================
const FollowupVisitService = {
    getAll: async () => {
        return await fetchAPI('/get_followup_visits/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_followup_visit/${id}`);
    },
    getByStudent: async (studentId) => {
        return await fetchAPI(`/get_followup_visits_by_student/${studentId}`);
    },
    getByTutor: async (tutorId) => {
        return await fetchAPI(`/get_followup_visits_by_tutor/${tutorId}`);
    },
    getPending: async (tutorId) => {
        return await fetchAPI(`/get_pending_visits/${tutorId}`);
    },
    create: async (data) => {
        return await fetchAPI('/create_followup_visit', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_followup_visit/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_followup_visit/${id}`, {
            method: 'DELETE'
        });
    },
    complete: async (id, report) => {
        return await fetchAPI(`/complete_followup_visit/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ report })
        });
    },
    reschedule: async (id, newDate) => {
        return await fetchAPI(`/reschedule_followup_visit/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ new_date: newDate })
        });
    }
};

// ============================================
// AGREEMENTS SERVICE (Convenios)
// ============================================
const AgreementService = {
    getAll: async () => {
        return await fetchAPI('/get_agreements/');
    },
    getById: async (id) => {
        return await fetchAPI(`/get_agreement/${id}`);
    },
    getByCompany: async (companyId) => {
        return await fetchAPI(`/get_agreements_by_company/${companyId}`);
    },
    getActive: async () => {
        return await fetchAPI('/get_active_agreements/');
    },
    create: async (data) => {
        return await fetchAPI('/create_agreement', {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },
    update: async (id, data) => {
        return await fetchAPI(`/update_agreement/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    delete: async (id) => {
        return await fetchAPI(`/delete_agreement/${id}`, {
            method: 'DELETE'
        });
    },
    sign: async (id, signature) => {
        return await fetchAPI(`/sign_agreement/${id}`, {
            method: 'PUT',
            body: JSON.stringify({ signature })
        });
    }
};

// ============================================
// DASHBOARD SERVICE
// ============================================
const DashboardService = {
    getAdminStats: async () => {
        return await fetchAPI('/get_admin_stats/');
    },
    getTutorStats: async (tutorId) => {
        return await fetchAPI(`/get_tutor_stats/${tutorId}`);
    },
    getStudentStats: async (studentId) => {
        return await fetchAPI(`/get_student_stats/${studentId}`);
    },
    getCompanyStats: async (companyId) => {
        return await fetchAPI(`/get_company_stats/${companyId}`);
    },
    getRecentActivity: async () => {
        return await fetchAPI('/get_recent_activity/');
    },
    getCharts: async () => {
        return await fetchAPI('/get_charts_data/');
    }
};

// ============================================
// PROFILE SERVICE
// ============================================
const ProfileService = {
    getMyProfile: async () => {
        const user = AuthService.getCurrentUser();
        return await fetchAPI(`/get_profile/${user.id}`);
    },
    updateProfile: async (data) => {
        const user = AuthService.getCurrentUser();
        return await fetchAPI(`/update_profile/${user.id}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },
    uploadPhoto: async (file) => {
        const formData = new FormData();
        formData.append('photo', file);
        const user = AuthService.getCurrentUser();
        const response = await fetch(`${API_BASE_URL}/upload_photo/${user.id}`, {
            method: 'POST',
            body: formData
        });
        return await response.json();
    },
    getActivityLog: async () => {
        const user = AuthService.getCurrentUser();
        return await fetchAPI(`/get_activity_log/${user.id}`);
    }
};

// ============================================
// EXPORTAR TODOS LOS SERVICIOS
// ============================================
window.AuthService = AuthService;
window.StudentService = StudentService;
window.TutorService = TutorService;
window.CompanyService = CompanyService;
window.OfferService = OfferService;
window.ApplicationService = ApplicationService;
window.AssignmentService = AssignmentService;
window.EvaluationService = EvaluationService;
window.UserService = UserService;
window.ReportService = ReportService;
window.NotificationService = NotificationService;
window.FollowupVisitService = FollowupVisitService;
window.AgreementService = AgreementService;
window.DashboardService = DashboardService;
window.ProfileService = ProfileService;