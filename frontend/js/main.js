// ============================================
// INTERNSYS - FUNCIONES PRINCIPALES
// ============================================

// Inicializar tooltips de Bootstrap
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Formatear fecha
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

// Formatear moneda
function formatMoney(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Formatear número con separadores
function formatNumber(number) {
    return new Intl.NumberFormat('es-ES').format(number);
}

// Generar ID único
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Descargar archivo
function downloadFile(content, fileName, contentType) {
    const a = document.createElement('a');
    const file = new Blob([content], { type: contentType });
    a.href = URL.createObjectURL(file);
    a.download = fileName;
    a.click();
    URL.revokeObjectURL(a.href);
}

// Exportar tabla a Excel
function exportToExcel(tableId, fileName) {
    const table = document.getElementById(tableId);
    const rows = table.querySelectorAll('tr');
    let csv = [];
    
    for (let i = 0; i < rows.length; i++) {
        const row = [], cols = rows[i].querySelectorAll('td, th');
        for (let j = 0; j < cols.length; j++) {
            let data = cols[j].innerText.replace(/,/g, '');
            row.push(data);
        }
        csv.push(row.join(','));
    }
    
    const csvContent = csv.join('\n');
    downloadFile(csvContent, `${fileName}.csv`, 'text/csv');
}

// Exportar a PDF (requiere html2pdf)
async function exportToPDF(elementId, fileName) {
    const element = document.getElementById(elementId);
    if (typeof html2pdf !== 'undefined') {
        const opt = {
            margin: 1,
            filename: `${fileName}.pdf`,
            image: { type: 'jpeg', quality: 0.98 },
            html2canvas: { scale: 2 },
            jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    } else {
        window.print();
    }
}

// Copiar al portapapeles
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        if (typeof AlertComponent !== 'undefined') {
            AlertComponent.success('Copiado al portapapeles');
        }
    }).catch(() => {
        if (typeof AlertComponent !== 'undefined') {
            AlertComponent.error('Error al copiar');
        }
    });
}

// Debounce para búsquedas
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Validar cédula ecuatoriana
function validateCedula(cedula) {
    if (!/^\d{10}$/.test(cedula)) return false;
    
    const digits = cedula.split('').map(Number);
    const province = parseInt(cedula.substring(0, 2), 10);
    if (province < 1 || province > 24) return false;
    
    const lastDigit = digits.pop();
    let sum = 0;
    for (let i = 0; i < digits.length; i++) {
        let mul = i % 2 === 0 ? 2 : 1;
        let val = digits[i] * mul;
        sum += val > 9 ? val - 9 : val;
    }
    
    const checkDigit = (Math.ceil(sum / 10) * 10) - sum;
    return checkDigit === lastDigit;
}

// Validar email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Mostrar/ocultar contraseña
function togglePassword(inputId, iconId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(iconId);
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('fa-eye');
        icon.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('fa-eye-slash');
        icon.classList.add('fa-eye');
    }
}

// Cargar menú lateral según rol
function loadSidebarByRole() {
    const user = getCurrentUser();
    if (!user) return;
    
    const sidebarMenu = document.getElementById('sidebarMenu');
    if (!sidebarMenu) return;
    
    let menuItems = [];
    
    if (user.rol === 'admin') {
        menuItems = [
            { href: 'dashboard-admin.html', icon: 'fa-tachometer-alt', label: 'Dashboard' },
            { href: 'students.html', icon: 'fa-user-graduate', label: 'Estudiantes' },
            { href: 'companies.html', icon: 'fa-building', label: 'Empresas' },
            { href: 'tutors.html', icon: 'fa-chalkboard-user', label: 'Tutores' },
            { href: 'offers.html', icon: 'fa-briefcase', label: 'Ofertas' },
            { href: 'assignments.html', icon: 'fa-handshake', label: 'Asignaciones' },
            { href: 'users.html', icon: 'fa-users', label: 'Usuarios' },
            { href: 'agreements.html', icon: 'fa-file-signature', label: 'Convenios' },
            { href: 'followup.html', icon: 'fa-calendar-check', label: 'Visitas' },
            { href: 'evaluations.html', icon: 'fa-star', label: 'Evaluaciones' },
            { href: 'reports.html', icon: 'fa-chart-line', label: 'Reportes' },
            { href: 'notifications.html', icon: 'fa-bell', label: 'Notificaciones' },
            { href: 'my-profile.html', icon: 'fa-user', label: 'Mi Perfil' }
        ];
    } else if (user.rol === 'estudiante') {
        menuItems = [
            { href: 'dashboard-student.html', icon: 'fa-tachometer-alt', label: 'Dashboard' },
            { href: 'my-profile.html', icon: 'fa-user', label: 'Mi Perfil' },
            { href: 'my-assignments.html', icon: 'fa-tasks', label: 'Mis Asignaciones' },
            { href: 'my-evaluations.html', icon: 'fa-star', label: 'Mis Evaluaciones' },
            { href: 'offers.html', icon: 'fa-briefcase', label: 'Ofertas' }
        ];
    } else if (user.rol === 'tutor' || user.rol === 'docente') {
        menuItems = [
            { href: 'dashboard-tutor.html', icon: 'fa-tachometer-alt', label: 'Dashboard' },
            { href: 'my-students.html', icon: 'fa-users', label: 'Mis Estudiantes' },
            { href: 'evaluations.html', icon: 'fa-star', label: 'Evaluaciones' },
            { href: 'followup.html', icon: 'fa-calendar-check', label: 'Visitas' },
            { href: 'reports.html', icon: 'fa-chart-line', label: 'Reportes' },
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

// Inicializar todo al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    // Inicializar tooltips
    initTooltips();
    
    // Cargar menú lateral si existe
    if (document.getElementById('sidebarMenu')) {
        loadSidebarByRole();
    }
    
    // Configurar toggle sidebar
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