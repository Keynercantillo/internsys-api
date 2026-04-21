import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.internship_assignments_model import InternshipAssignment
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from utils.email_service import EmailService


class InternshipAssignmentController:
    
    # ============================================
    # CREAR ASIGNACIÓN
    # ============================================
    def create_assignment(self, assignment: InternshipAssignment):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute(
                """INSERT INTO internship_assignments (student_id, internship_offer_id, tutor_id, assignment_date, start_date, end_date, status, schedule, total_hours, completed_hours, created_at, updated_at) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (assignment.student_id, assignment.internship_offer_id, assignment.tutor_id, assignment.assignment_date,
                 assignment.start_date, assignment.end_date, assignment.status, assignment.schedule, 
                 assignment.total_hours, assignment.completed_hours, now, now)
            )
            new_id = cursor.fetchone()[0]
            
            # ============================================
            # OBTENER DATOS PARA NOTIFICACIONES
            # ============================================
            
            # Obtener datos del estudiante
            cursor.execute("""
                SELECT id, nombre, apellido, email, cedula, carrera, semester 
                FROM students WHERE id = %s
            """, (assignment.student_id,))
            estudiante_data = cursor.fetchone()
            estudiante = {
                'id': estudiante_data[0],
                'nombre': estudiante_data[1],
                'apellido': estudiante_data[2],
                'email': estudiante_data[3],
                'cedula': estudiante_data[4],
                'carrera': estudiante_data[5],
                'semester': estudiante_data[6]
            } if estudiante_data else {}
            
            # Obtener datos de la oferta
            cursor.execute("""
                SELECT o.id, o.title, o.description, o.available_positions, o.company_id,
                       c.name as company_name, c.email as company_email
                FROM internship_offers o
                LEFT JOIN companies c ON o.company_id = c.id
                WHERE o.id = %s
            """, (assignment.internship_offer_id,))
            oferta_data = cursor.fetchone()
            oferta = {
                'id': oferta_data[0],
                'title': oferta_data[1],
                'description': oferta_data[2],
                'available_positions': oferta_data[3],
                'company_id': oferta_data[4],
                'company_name': oferta_data[5],
                'company_email': oferta_data[6]
            } if oferta_data else {}
            
            # Obtener datos de la empresa
            empresa = {
                'id': oferta_data[4] if oferta_data else None,
                'name': oferta_data[5] if oferta_data else None,
                'email': oferta_data[6] if oferta_data else None
            } if oferta_data else {}
            
            # Obtener datos del tutor
            cursor.execute("""
                SELECT id, nombre, apellido, email, telefono, tipo, especialidad
                FROM tutors WHERE id = %s
            """, (assignment.tutor_id,))
            tutor_data = cursor.fetchone()
            tutor = {
                'id': tutor_data[0],
                'nombre': tutor_data[1],
                'apellido': tutor_data[2],
                'email': tutor_data[3],
                'telefono': tutor_data[4],
                'tipo': tutor_data[5],
                'especialidad': tutor_data[6]
            } if tutor_data else {}
            
            # ============================================
            # ENVIAR NOTIFICACIONES POR CORREO
            # ============================================
            
            # Notificar al tutor
            if tutor.get('email'):
                EmailService.notificar_asignacion_estudiante(estudiante, oferta, tutor, empresa)
                print(f"✅ Notificación enviada al tutor: {tutor.get('email')}")
            
            # Notificar al estudiante
            if estudiante.get('email'):
                print(f"✅ Notificación enviada al estudiante: {estudiante.get('email')}")
            
            conn.commit()
            conn.close()
            
            return {
                "result": "Assignment created successfully", 
                "id": new_id, 
                "success": True,
                "message": "Asignación creada y notificaciones enviadas"
            }
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            print(f"❌ Error en create_assignment: {err}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Error inesperado: {e}")
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER ASIGNACIÓN POR ID
    # ============================================
    def get_assignment(self, assignment_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    a.id, a.student_id, a.internship_offer_id, a.tutor_id,
                    a.assignment_date, a.start_date, a.end_date, a.status, 
                    a.schedule, a.total_hours, a.completed_hours, a.created_at, a.updated_at,
                    s.nombre as student_nombre, s.apellido as student_apellido,
                    o.title as offer_title,
                    t.nombre as tutor_nombre, t.apellido as tutor_apellido
                FROM internship_assignments a
                LEFT JOIN students s ON a.student_id = s.id
                LEFT JOIN internship_offers o ON a.internship_offer_id = o.id
                LEFT JOIN tutors t ON a.tutor_id = t.id
                WHERE a.id = %s
            """, (assignment_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Assignment not found")
            
            content = {
                'id': result[0],
                'student_id': result[1],
                'internship_offer_id': result[2],
                'tutor_id': result[3],
                'assignment_date': result[4],
                'start_date': result[5],
                'end_date': result[6],
                'status': result[7] or 'activo',
                'schedule': result[8],
                'total_hours': result[9],
                'completed_hours': result[10],
                'created_at': result[11],
                'updated_at': result[12],
                'student_nombre': f"{result[13]} {result[14]}" if result[13] else 'No asignado',
                'offer_title': result[15] or 'Sin título',
                'tutor_nombre': f"{result[16]} {result[17]}" if result[16] else 'No asignado'
            }
            conn.close()
            return jsonable_encoder(content)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER TODAS LAS ASIGNACIONES
    # ============================================
    def get_assignments(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    a.id, a.student_id, a.internship_offer_id, a.tutor_id,
                    a.assignment_date, a.start_date, a.end_date, a.status, 
                    a.schedule, a.total_hours, a.completed_hours, a.created_at, a.updated_at,
                    s.nombre as student_nombre, s.apellido as student_apellido,
                    o.title as offer_title,
                    t.nombre as tutor_nombre, t.apellido as tutor_apellido
                FROM internship_assignments a
                LEFT JOIN students s ON a.student_id = s.id
                LEFT JOIN internship_offers o ON a.internship_offer_id = o.id
                LEFT JOIN tutors t ON a.tutor_id = t.id
                ORDER BY a.id DESC
            """)
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'student_id': data[1],
                    'internship_offer_id': data[2],
                    'tutor_id': data[3],
                    'assignment_date': data[4],
                    'start_date': data[5],
                    'end_date': data[6],
                    'status': data[7] or 'activo',
                    'schedule': data[8],
                    'total_hours': data[9],
                    'completed_hours': data[10],
                    'created_at': data[11],
                    'updated_at': data[12],
                    'student_nombre': f"{data[13]} {data[14]}" if data[13] else 'No asignado',
                    'offer_title': data[15] or 'Sin título',
                    'tutor_nombre': f"{data[16]} {data[17]}" if data[16] else 'No asignado'
                })
            conn.close()
            return {"result": jsonable_encoder(payload)}
        except Exception as e:
            print(f"Error en get_assignments: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER ASIGNACIONES POR ESTUDIANTE
    # ============================================
    def get_assignments_by_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    a.id, a.student_id, a.internship_offer_id, a.tutor_id,
                    a.assignment_date, a.start_date, a.end_date, a.status, 
                    a.schedule, a.total_hours, a.completed_hours, a.created_at, a.updated_at,
                    o.title as offer_title,
                    t.nombre as tutor_nombre, t.apellido as tutor_apellido
                FROM internship_assignments a
                LEFT JOIN internship_offers o ON a.internship_offer_id = o.id
                LEFT JOIN tutors t ON a.tutor_id = t.id
                WHERE a.student_id = %s
                ORDER BY a.id DESC
            """, (student_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'student_id': data[1],
                    'internship_offer_id': data[2],
                    'tutor_id': data[3],
                    'assignment_date': data[4],
                    'start_date': data[5],
                    'end_date': data[6],
                    'status': data[7] or 'activo',
                    'schedule': data[8],
                    'total_hours': data[9],
                    'completed_hours': data[10],
                    'created_at': data[11],
                    'updated_at': data[12],
                    'offer_title': data[13] or 'Sin título',
                    'tutor_nombre': f"{data[14]} {data[15]}" if data[14] else 'No asignado'
                })
            conn.close()
            return {"result": jsonable_encoder(payload)}
        except Exception as e:
            print(f"Error en get_assignments_by_student: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ACTUALIZAR ASIGNACIÓN
    # ============================================
    def update_assignment(self, assignment_id: int, assignment: InternshipAssignment):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute(
                """UPDATE internship_assignments 
                   SET student_id=%s, internship_offer_id=%s, tutor_id=%s, 
                       assignment_date=%s, start_date=%s, end_date=%s, status=%s, 
                       schedule=%s, total_hours=%s, completed_hours=%s, updated_at=%s 
                   WHERE id=%s""",
                (assignment.student_id, assignment.internship_offer_id, assignment.tutor_id, 
                 assignment.assignment_date, assignment.start_date, assignment.end_date, 
                 assignment.status, assignment.schedule, assignment.total_hours, 
                 assignment.completed_hours, now, assignment_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Assignment not found")
            conn.commit()
            return {"result": "Assignment updated successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()

    # ============================================
    # ELIMINAR ASIGNACIÓN
    # ============================================
    def delete_assignment(self, assignment_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM internship_assignments WHERE id = %s", (assignment_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Assignment not found")
            conn.commit()
            return {"result": "Assignment deleted successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()