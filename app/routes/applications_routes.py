from fastapi import APIRouter, HTTPException, Query
from controllers.applications_controller import ApplicationsController
from models.applications_model import Application
from typing import Optional
from datetime import date

router = APIRouter()
applications_controller = ApplicationsController()

# ============================================
# CREAR POSTULACIÓN
# ============================================
@router.post("/create_application")
async def create_application(application: Application):
    """Crear una nueva postulación a una oferta"""
    return applications_controller.create_application(application)

# ============================================
# OBTENER TODAS LAS POSTULACIONES
# ============================================
@router.get("/get_applications")
async def get_applications():
    """Obtener todas las postulaciones del sistema"""
    return applications_controller.get_applications()

# ============================================
# OBTENER POSTULACIONES POR OFERTA (NUEVO - PARA VER POSTULANTES)
# ============================================
@router.get("/get_applications_by_offer/{offer_id}")
async def get_applications_by_offer(offer_id: int):
    """
    Obtener todas las postulaciones de una oferta específica.
    Útil para que el admin/empresa vea quiénes aplicaron a una oferta.
    """
    try:
        from config.db_config import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT a.id, a.offer_id, a.student_id, a.empresa_id, a.tutor_id, 
                   a.status, a.application_date, a.comments, a.created_at,
                   s.id as student_id, s.nombre as student_nombre, s.apellido as student_apellido, 
                   s.cedula, s.carrera, s.semester,
                   c.name as empresa_nombre,
                   t.nombre as tutor_nombre, t.apellido as tutor_apellido
            FROM applications a
            LEFT JOIN students s ON a.student_id = s.id
            LEFT JOIN companies c ON a.empresa_id = c.id
            LEFT JOIN tutors t ON a.tutor_id = t.id
            WHERE a.offer_id = %s
            ORDER BY a.application_date DESC
        """, (offer_id,))
        
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        applications = []
        for row in result:
            applications.append({
                'id': row[0],
                'offer_id': row[1],
                'student_id': row[2],
                'empresa_id': row[3],
                'tutor_id': row[4],
                'status': row[5],
                'application_date': row[6].isoformat() if row[6] else None,
                'comments': row[7],
                'created_at': row[8].isoformat() if row[8] else None,
                'student_name': f"{row[10]} {row[11]}" if row[10] else 'No especificado',
                'student_cedula': row[12] or '-',
                'student_carrera': row[13] or 'No especificada',
                'student_semester': row[14],
                'empresa_nombre': row[15] or '-',
                'tutor_name': f"{row[16]} {row[17]}" if row[16] else 'No asignado'
            })
        
        return {"success": True, "result": applications}
        
    except Exception as e:
        print(f"Error en get_applications_by_offer: {e}")
        return {"success": False, "result": [], "error": str(e)}

# ============================================
# OBTENER POSTULACIONES POR EMPRESA
# ============================================
@router.get("/get_applications_by_company/{empresa_id}")
async def get_applications_by_company(empresa_id: int):
    """Obtener todas las postulaciones de una empresa específica"""
    return applications_controller.get_applications_by_company(empresa_id)

# ============================================
# OBTENER POSTULACIONES POR ESTUDIANTE
# ============================================
@router.get("/get_applications_by_student/{student_id}")
async def get_applications_by_student(student_id: int):
    """Obtener todas las postulaciones de un estudiante específico"""
    return applications_controller.get_applications_by_student(student_id)

# ============================================
# OBTENER POSTULACIÓN POR ID
# ============================================
@router.get("/get_application/{application_id}")
async def get_application_by_id(application_id: int):
    """Obtener una postulación específica por su ID"""
    return applications_controller.get_application_by_id(application_id)

# ============================================
# ACTUALIZAR ESTADO DE POSTULACIÓN (ACEPTAR/RECHAZAR)
# ============================================
@router.put("/update_application_status/{application_id}")
async def update_application_status(
    application_id: int, 
    status: str = Query(..., description="nuevo estado: pendiente, aceptada, rechazada"),
    tutor_id: Optional[int] = Query(None, description="ID del tutor asignado (opcional)")
):
    """
    Actualizar el estado de una postulación.
    Estados posibles: pendiente, aceptada, rechazada
    """
    return applications_controller.update_application_status(application_id, status, tutor_id)

# ============================================
# ELIMINAR POSTULACIÓN
# ============================================
@router.delete("/delete_application/{application_id}")
async def delete_application(application_id: int):
    """Eliminar una postulación"""
    return applications_controller.delete_application(application_id)

# ============================================
# CONTAR POSTULACIONES POR OFERTA
# ============================================
@router.get("/count_applications_by_offer/{offer_id}")
async def count_applications_by_offer(offer_id: int):
    """Contar cuántas postulaciones tiene una oferta"""
    try:
        from config.db_config import get_db_connection
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM applications WHERE offer_id = %s
        """, (offer_id,))
        
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        return {"success": True, "count": count}
        
    except Exception as e:
        return {"success": False, "count": 0, "error": str(e)}