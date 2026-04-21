import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.applications_model import Application
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from utils.email_service import EmailService


class ApplicationsController:
    
    # ============================================
    # CREAR POSTULACIÓN
    # ============================================
    def create_application(self, application: Application):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute("""
                INSERT INTO applications (offer_id, student_id, empresa_id, tutor_id, status, application_date, comments, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (application.offer_id, application.student_id, application.empresa_id, 
                  application.tutor_id, application.status, application.application_date, 
                  application.comments, now, now))
            
            new_id = cursor.fetchone()[0]
            
            # ============================================
            # OBTENER DATOS PARA NOTIFICACIONES
            # ============================================
            
            # Obtener datos del estudiante
            cursor.execute("""
                SELECT id, nombre, apellido, email, carrera, cedula 
                FROM students WHERE id = %s
            """, (application.student_id,))
            estudiante_data = cursor.fetchone()
            estudiante = {
                'id': estudiante_data[0],
                'nombre': estudiante_data[1],
                'apellido': estudiante_data[2],
                'email': estudiante_data[3],
                'carrera': estudiante_data[4],
                'cedula': estudiante_data[5]
            } if estudiante_data else {}
            
            # Obtener datos de la oferta
            cursor.execute("""
                SELECT o.id, o.title, o.description, o.available_positions, o.company_id,
                       c.name as company_name, c.email as company_email
                FROM internship_offers o
                LEFT JOIN companies c ON o.company_id = c.id
                WHERE o.id = %s
            """, (application.offer_id,))
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
            
            # Datos de la empresa
            empresa = {
                'id': application.empresa_id,
                'name': oferta_data[5] if oferta_data else None,
                'email': oferta_data[6] if oferta_data else None
            }
            
            # ============================================
            # ENVIAR NOTIFICACIONES POR CORREO
            # ============================================
            
            if empresa.get('email'):
                EmailService.notificar_postulacion_estudiante(estudiante, oferta, empresa)
                print(f"✅ Notificación enviada a la empresa: {empresa.get('email')}")
            
            if estudiante.get('email'):
                print(f"✅ Notificación enviada al estudiante: {estudiante.get('email')}")
            
            conn.commit()
            conn.close()
            
            return {
                "result": "Application created successfully", 
                "id": new_id, 
                "success": True,
                "message": "Postulación creada y notificaciones enviadas"
            }
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            print(f"❌ Error en create_application: {err}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER POSTULACIONES POR EMPRESA
    # ============================================
    def get_applications_by_company(self, empresa_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.offer_id, a.student_id, a.empresa_id, a.tutor_id, 
                       a.status, a.application_date, a.comments, a.created_at, a.updated_at,
                       o.title as offer_title,
                       s.nombre as student_nombre, s.apellido as student_apellido,
                       s.carrera as student_carrera,
                       t.nombre as tutor_nombre, t.apellido as tutor_apellido
                FROM applications a
                LEFT JOIN internship_offers o ON a.offer_id = o.id
                LEFT JOIN students s ON a.student_id = s.id
                LEFT JOIN tutors t ON a.tutor_id = t.id
                WHERE a.empresa_id = %s
                ORDER BY a.application_date DESC
            """, (empresa_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'offer_id': data[1],
                    'student_id': data[2],
                    'empresa_id': data[3],
                    'tutor_id': data[4],
                    'status': data[5],
                    'application_date': data[6],
                    'comments': data[7],
                    'created_at': data[8],
                    'updated_at': data[9],
                    'offer_title': data[10] or 'Sin título',
                    'student_nombre': f"{data[11]} {data[12]}" if data[11] else 'No especificado',
                    'student_carrera': data[13] or 'N/A',
                    'tutor_nombre': f"{data[14]} {data[15]}" if data[14] else 'No asignado'
                })
            conn.close()
            return {"result": jsonable_encoder(payload)}
        except Exception as e:
            print(f"Error en get_applications_by_company: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER TODAS LAS POSTULACIONES
    # ============================================
    def get_applications(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.id, a.offer_id, a.student_id, a.empresa_id, a.tutor_id, 
                       a.status, a.application_date, a.comments, a.created_at, a.updated_at,
                       o.title as offer_title,
                       s.nombre as student_nombre, s.apellido as student_apellido,
                       c.name as empresa_nombre
                FROM applications a
                LEFT JOIN internship_offers o ON a.offer_id = o.id
                LEFT JOIN students s ON a.student_id = s.id
                LEFT JOIN companies c ON a.empresa_id = c.id
                ORDER BY a.application_date DESC
            """)
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'offer_id': data[1],
                    'student_id': data[2],
                    'empresa_id': data[3],
                    'tutor_id': data[4],
                    'status': data[5],
                    'application_date': data[6],
                    'comments': data[7],
                    'created_at': data[8],
                    'updated_at': data[9],
                    'offer_title': data[10] or 'Sin título',
                    'student_nombre': f"{data[11]} {data[12]}" if data[11] else 'No especificado',
                    'empresa_nombre': data[13] or 'No especificada'
                })
            conn.close()
            return {"result": jsonable_encoder(payload)}
        except Exception as e:
            print(f"Error en get_applications: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ACTUALIZAR ESTADO DE POSTULACIÓN
    # ============================================
    def update_application_status(self, application_id: int, status: str, tutor_id: int = None):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute("""
                UPDATE applications 
                SET status=%s, tutor_id=%s, updated_at=%s 
                WHERE id=%s
            """, (status, tutor_id, now, application_id))
            
            conn.commit()
            conn.close()
            return {"result": "Application updated successfully", "success": True}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ELIMINAR POSTULACIÓN
    # ============================================
    def delete_application(self, application_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM applications WHERE id = %s", (application_id,))
            conn.commit()
            conn.close()
            return {"result": "Application deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()