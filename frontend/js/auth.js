// ============================================
// INTERNSYS - SISTEMA DE AUTENTICACIÓN
// ============================================

const AUTH_KEY = 'internsys_user';
const API_URL = 'http://127.0.0.1:8000/api';

// ============================================
// USUARIOS DE PRUEBA (FALLBACK)
// ============================================
const TEST_USERS = {
    'admin@internsys.com': {
        password: 'admin123',
        nombre: 'Admin',
        apellido: 'Sistema',
        cedula: '12345678',
        edad: 30,
        usuario: 'admin',
        rol: 'admin',
        email: 'admin@internsys.com',
        id: 1,
        is_active: true,
        empresa_id: null
    },
    'estudiante@universidad.edu': {
        password: 'estudiante123',
        nombre: 'María',
        apellido: 'López',
        cedula: '11122233',
        edad: 22,
        usuario: 'maria.lopez',
        rol: 'estudiante',
        email: 'estudiante@universidad.edu',
        id: 2,
        matricula: '20240001',
        carrera: 'Ingeniería de Sistemas',
        semester: 6,
        promedio: 4.5,
        empresa_id: null
    },
    'tutor@empresa.com': {
        password: 'tutor123',
        nombre: 'Carlos',
        apellido: 'Gómez',
        cedula: '87654321',
        edad: 35,
        usuario: 'carlos.gomez',
        rol: 'tutor',
        email: 'tutor@empresa.com',
        id: 3,
        tipo: 'empresarial',
        telefono: '555-1234',
        empresa: 'Tech Solutions',
        empresa_id: 1
    },
    'profesor@universidad.edu': {
        password: 'profesor123',
        nombre: 'Ana',
        apellido: 'Martínez',
        cedula: '44455566',
        edad: 45,
        usuario: 'ana.martinez',
        rol: 'docente',
        email: 'profesor@universidad.edu',
        id: 4,
        tipo: 'academico',
        departamento: 'Ingeniería',
        empresa_id: null
    },
    'empresa@techsolutions.com': {
        password: 'empresa123',
        nombre: 'Tech',
        apellido: 'Solutions',
        cedula: '99988877',
        edad: 40,
        usuario: 'techsolutions',
        rol: 'empresa',
        email: 'empresa@techsolutions.com',
        id: 5,
        empresa_id: 1,
        empresa_nombre: 'Tech Solutions S.A.',
        ruc: '999888777',
        telefono: '555-9999',
        direccion: 'Av. Tecnológica 456'
    }
};

// ============================================
// FUNCIONES DE UTILIDAD
// ============================================

function showAlertMessage(message, type = 'success') {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: type === 'success' ? 'Éxito' : type === 'error' ? 'Error' : 'Información',
            text: message,
            icon: type,
            confirmButtonColor: '#9b59b6',
            timer: 2000,
            timerProgressBar: true
        });
    } else if (typeof AlertComponent !== 'undefined') {
        if (type === 'success') AlertComponent.success(message);
        else if (type === 'error') AlertComponent.error(message);
        else if (type === 'warning') AlertComponent.warning(message);
        else AlertComponent.info(message);
    } else {
        alert(message);
    }
}

function getRoleByEmail(email) {
    if (!email) return null;
    email = email.toLowerCase();
    if (email.includes('admin')) return 'admin';
    if (email.includes('empresa') || email.includes('@empresa') || email.includes('@company')) return 'empresa';
    if (email.includes('estudiante') || email.includes('@universidad.edu') || email.includes('@alumno')) return 'estudiante';
    if (email.includes('tutor') || email.includes('@empresa.com')) return 'tutor';
    if (email.includes('profesor') || email.includes('docente')) return 'docente';
    return 'estudiante';
}

// ============================================
// DASHBOARD SEGÚN ROL
// ============================================

function getDashboardByRole(rol) {
    const dashboards = {
        'admin': 'dashboard-admin.html',
        'estudiante': 'dashboard-student.html',
        'tutor': 'dashboard-tutor.html',
        'docente': 'dashboard-tutor.html',
        'empresa': 'dashboard-company.html'
    };
    return dashboards[rol] || 'dashboard-student.html';
}

// ============================================
// PERMISOS SEGÚN ROL
// ============================================

function getUserPermissions(rol) {
    const permissions = {
        'admin': {
            canCreate: true,
            canEdit: true,
            canDelete: true,
            canViewAll: true,
            canExport: true,
            modules: ['students', 'companies', 'tutors', 'offers', 'assignments', 'users', 'agreements', 'followup', 'evaluations', 'reports']
        },
        'tutor': {
            canCreate: true,
            canEdit: true,
            canDelete: false,
            canViewAll: false,
            canExport: true,
            modules: ['students', 'offers', 'assignments', 'followup', 'evaluations']
        },
        'docente': {
            canCreate: true,
            canEdit: true,
            canDelete: false,
            canViewAll: false,
            canExport: true,
            modules: ['students', 'evaluations', 'reports']
        },
        'estudiante': {
            canCreate: false,
            canEdit: true,
            canDelete: false,
            canViewAll: false,
            canExport: false,
            modules: ['myProfile', 'myAssignments', 'myEvaluations', 'offers']
        },
        'empresa': {
            canCreate: true,
            canEdit: true,
            canDelete: false,
            canViewAll: false,
            canExport: true,
            modules: ['myOffers', 'myAssignments', 'myCompany', 'applications']
        }
    };
    return permissions[rol] || permissions['estudiante'];
}

// ============================================
// LOGIN
// ============================================

async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        
        if (response.ok) {
            const data = await response.json();
            const user = data.result;
            
            const userData = {
                id: user.id,
                nombre: user.nombre,
                apellido: user.apellido,
                cedula: user.cedula,
                edad: user.edad,
                usuario: user.usuario,
                email: user.email,
                rol: user.rol,
                empresa_id: user.empresa_id || null,
                permissions: getUserPermissions(user.rol),
                dashboard: getDashboardByRole(user.rol)
            };
            
            localStorage.setItem(AUTH_KEY, JSON.stringify(userData));
            console.log('Usuario guardado:', userData);
            showAlertMessage(`Bienvenido ${user.nombre} ${user.apellido} (${user.rol})`, 'success');
            
            setTimeout(() => { window.location.href = userData.dashboard; }, 1000);
            return { success: true, user: userData };
        }
        
        // Fallback a usuarios de prueba
        const user = TEST_USERS[email.toLowerCase()];
        if (user && user.password === password) {
            const userData = {
                id: user.id,
                nombre: user.nombre,
                apellido: user.apellido,
                cedula: user.cedula,
                edad: user.edad,
                usuario: user.usuario,
                email: user.email,
                rol: user.rol,
                empresa_id: user.empresa_id || null,
                permissions: getUserPermissions(user.rol),
                dashboard: getDashboardByRole(user.rol),
                ...user
            };
            localStorage.setItem(AUTH_KEY, JSON.stringify(userData));
            showAlertMessage(`Bienvenido ${user.nombre} ${user.apellido} (${user.rol})`, 'success');
            setTimeout(() => { window.location.href = userData.dashboard; }, 1000);
            return { success: true, user: userData };
        } else {
            showAlertMessage('Correo o contraseña incorrectos', 'error');
            return { success: false };
        }
    } catch (error) {
        console.error('Login error:', error);
        const user = TEST_USERS[email.toLowerCase()];
        if (user && user.password === password) {
            const userData = {
                id: user.id,
                nombre: user.nombre,
                apellido: user.apellido,
                cedula: user.cedula,
                edad: user.edad,
                usuario: user.usuario,
                email: user.email,
                rol: user.rol,
                empresa_id: user.empresa_id || null,
                permissions: getUserPermissions(user.rol),
                dashboard: getDashboardByRole(user.rol),
                ...user
            };
            localStorage.setItem(AUTH_KEY, JSON.stringify(userData));
            showAlertMessage(`Bienvenido ${user.nombre} ${user.apellido} (${user.rol})`, 'success');
            setTimeout(() => { window.location.href = userData.dashboard; }, 1000);
            return { success: true, user: userData };
        }
        showAlertMessage('Error de conexión. Intente más tarde.', 'error');
        return { success: false };
    }
}

// ============================================
// FUNCIONES DE SESIÓN
// ============================================

function getCurrentUser() {
    const user = localStorage.getItem(AUTH_KEY);
    return user ? JSON.parse(user) : null;
}

function isAuthenticated() {
    return getCurrentUser() !== null;
}

function logout() {
    localStorage.removeItem(AUTH_KEY);
    showAlertMessage('Sesión cerrada exitosamente', 'info');
    setTimeout(() => { window.location.href = 'index.html'; }, 1000);
}

function checkAuth() {
    const user = getCurrentUser();
    const currentPage = window.location.pathname;
    
    if (currentPage.includes('index.html') || currentPage === '/' || currentPage === '') {
        return true;
    }
    
    if (!user) {
        window.location.href = 'index.html';
        return false;
    }
    
    // Admin puede acceder a todo
    if (user.rol === 'admin') return true;
    
    // Verificar acceso según rol
    if (user.rol === 'estudiante') {
        if (currentPage.includes('dashboard-admin.html') || currentPage.includes('companies.html') || 
            currentPage.includes('tutors.html') || currentPage.includes('assignments.html') || 
            currentPage.includes('users.html')) {
            window.location.href = 'dashboard-student.html';
            return false;
        }
    }
    
    if (user.rol === 'tutor' || user.rol === 'docente') {
        if (currentPage.includes('dashboard-admin.html') || currentPage.includes('students.html') || 
            currentPage.includes('companies.html') || currentPage.includes('users.html')) {
            window.location.href = 'dashboard-tutor.html';
            return false;
        }
    }
    
    if (user.rol === 'empresa') {
        if (currentPage.includes('dashboard-admin.html') || currentPage.includes('students.html') || 
            currentPage.includes('tutors.html') || currentPage.includes('dashboard-student.html') ||
            currentPage.includes('dashboard-tutor.html') || currentPage.includes('my-students.html')) {
            window.location.href = 'dashboard-company.html';
            return false;
        }
    }
    
    return true;
}

function hasPermission(module) {
    const user = getCurrentUser();
    if (!user) return false;
    return user.permissions.modules.includes(module);
}

function getToken() {
    const user = getCurrentUser();
    return user ? btoa(JSON.stringify(user)) : null;
}

// ============================================
// MENÚ LATERAL SEGÚN ROL
// ============================================

function loadSidebarByRole() {
    const user = getCurrentUser();
    if (!user) return;
    
    const sidebarMenu = document.getElementById('sidebarMenu');
    if (!sidebarMenu) return;
    
    let menuItems = [];
    
    // Menú para ADMIN
    if (user.rol === 'admin') {
        menuItems = [
            { href: 'dashboard-admin.html', icon: 'fa-tachometer-alt', label: 'Dashboard' },
            { href: 'students.html', icon: 'fa-user-graduate', label: 'Estudiantes' },
            { href: 'companies.html', icon: 'fa-building', label: 'Empresas' },
            { href: 'tutors.html', icon: 'fa-chalkboard-user', label: 'Tutores' },
            { href: 'offers.html', icon: 'fa-briefcase', label: 'Ofertas' },
            { href: 'assignments.html', icon: 'fa-handshake', label: 'Asignaciones' },
            { href: 'users.html', icon: 'fa-users', label: 'Usuarios' },
            { href: 'my-profile.html', icon: 'fa-user', label: 'Mi Perfil' }
        ];
    } 
    // Menú para ESTUDIANTE
    else if (user.rol === 'estudiante') {
        menuItems = [
            { href: 'dashboard-student.html', icon: 'fa-tachometer-alt', label: 'Mi Dashboard' },
            { href: 'my-profile.html', icon: 'fa-user', label: 'Mi Perfil' },
            { href: 'my-assignments.html', icon: 'fa-tasks', label: 'Mis Asignaciones' },
            { href: 'my-evaluations.html', icon: 'fa-star', label: 'Mis Evaluaciones' },
            { href: 'offers.html', icon: 'fa-briefcase', label: 'Ofertas' }
        ];
    }
    // Menú para TUTOR y DOCENTE
    else if (user.rol === 'tutor' || user.rol === 'docente') {
        menuItems = [
            { href: 'dashboard-tutor.html', icon: 'fa-tachometer-alt', label: 'Dashboard' },
            { href: 'my-students.html', icon: 'fa-users', label: 'Mis Estudiantes' },
            { href: 'evaluations.html', icon: 'fa-star', label: 'Evaluaciones' },
            { href: 'followup.html', icon: 'fa-calendar-check', label: 'Visitas' },
            { href: 'my-profile.html', icon: 'fa-user', label: 'Mi Perfil' }
        ];
    }
    // Menú para EMPRESA
    else if (user.rol === 'empresa') {
        menuItems = [
            { href: 'dashboard-company.html', icon: 'fa-tachometer-alt', label: 'Dashboard' },
            { href: 'company-offers.html', icon: 'fa-briefcase', label: 'Mis Ofertas' },
            { href: 'company-assignments.html', icon: 'fa-handshake', label: 'Mis Asignaciones' },
            { href: 'company-applications.html', icon: 'fa-file-alt', label: 'Postulaciones' },
            { href: 'company-profile.html', icon: 'fa-building', label: 'Mi Empresa' },
            { href: 'my-profile.html', icon: 'fa-user', label: 'Mi Perfil' }
        ];
    }
    
    sidebarMenu.innerHTML = menuItems.map(item => `
        <li>
            <a href="${item.href}" class="menu-item ${window.location.pathname.includes(item.href) ? 'active' : ''}">
                <i class="fas ${item.icon}"></i> ${item.label}
            </a>
        </li>
    `).join('');
}

// ============================================
// INICIALIZACIÓN
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await login(email, password);
        });
    }
    
    if ((window.location.pathname.includes('index.html') || window.location.pathname === '/' || window.location.pathname === '') && isAuthenticated()) {
        const user = getCurrentUser();
        window.location.href = user.dashboard;
    }
    
    if (document.getElementById('sidebarMenu')) {
        loadSidebarByRole();
    }
    
    const toggleBtn = document.getElementById('toggleSidebar');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.getElementById('mainContent');
            if (sidebar && mainContent) {
                sidebar.classList.toggle('closed');
                mainContent.classList.toggle('expanded');
            }
        });
    }
});

// ============================================
// EXPORTAR FUNCIONES (GLOBALES)
// ============================================

window.getCurrentUser = getCurrentUser;
window.isAuthenticated = isAuthenticated;
window.logout = logout;
window.checkAuth = checkAuth;
window.hasPermission = hasPermission;
window.getToken = getToken;
window.loadSidebarByRole = loadSidebarByRole;