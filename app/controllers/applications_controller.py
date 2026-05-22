import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.applications_model import Application
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from typing import Optional

class ApplicationsController:
    
    def __init__(self):
        pass
    
    # ============================================
    # CREAR POSTULACIÓN
    # ============================================
    def create_application(self, application: Application):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            # Verificar si ya postuló
            cursor.execute(
                "SELECT id FROM applications WHERE offer_id = %s AND student_id = %s",
                (application.offer_id, application.student_id)
            )
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Ya has postulado a esta oferta")
            
            # Insertar postulación
            cursor.execute("""
                INSERT INTO applications (offer_id, student_id, empresa_id, tutor_id, status, application_date, comments, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            """, (
                application.offer_id,
                application.student_id,
                application.empresa_id,
                application.tutor_id,
                "pendiente",
                application.application_date,
                application.comments,
                now,
                now
            ))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                "success": True,
                "message": "Postulación creada exitosamente",
                "result": {"id": new_id}
            }
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
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
            cursor.close()
            conn.close()
            
            applications = []
            for row in result:
                applications.append({
                    'id': row[0],
                    'offer_id': row[1],
                    'offer_title': row[10] if len(row) > 10 else 'Sin título',
                    'student_id': row[2],
                    'student_name': f"{row[11]} {row[12]}" if len(row) > 12 and row[11] else 'No especificado',
                    'empresa_id': row[3],
                    'empresa_name': row[13] if len(row) > 13 else '-',
                    'tutor_id': row[4],
                    'status': row[5],
                    'application_date': row[6].isoformat() if row[6] else None,
                    'comments': row[7],
                    'created_at': row[8].isoformat() if row[8] else None
                })
            
            return {"success": True, "result": applications}
            
        except Exception as e:
            print(f"Error en get_applications: {e}")
            return {"success": True, "result": []}
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
                SELECT a.id, a.offer_id, o.title as offer_title, a.student_id, 
                       s.nombre as student_nombre, s.apellido as student_apellido,
                       a.status, a.application_date, a.comments
                FROM applications a
                LEFT JOIN internship_offers o ON a.offer_id = o.id
                LEFT JOIN students s ON a.student_id = s.id
                WHERE a.empresa_id = %s
                ORDER BY a.application_date DESC
            """, (empresa_id,))
            
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            
            applications = []
            for row in result:
                applications.append({
                    'id': row[0],
                    'offer_id': row[1],
                    'offer_title': row[2] or 'Sin título',
                    'student_id': row[3],
                    'student_name': f"{row[4]} {row[5]}" if row[4] else 'No especificado',
                    'status': row[6],
                    'application_date': row[7].isoformat() if row[7] else None,
                    'comments': row[8]
                })
            
            return {"success": True, "result": applications}
            
        except Exception as e:
            print(f"Error en get_applications_by_company: {e}")
            return {"success": True, "result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER POSTULACIONES POR ESTUDIANTE
    # ============================================
    def get_applications_by_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT a.id, a.offer_id, o.title as offer_title, c.name as company_name,
                       a.status, a.application_date, a.comments, a.created_at
                FROM applications a
                LEFT JOIN internship_offers o ON a.offer_id = o.id
                LEFT JOIN companies c ON a.empresa_id = c.id
                WHERE a.student_id = %s
                ORDER BY a.application_date DESC
            """, (student_id,))
            
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            
            applications = []
            for row in result:
                applications.append({
                    'id': row[0],
                    'offer_id': row[1],
                    'offer_title': row[2] or 'Sin título',
                    'company_name': row[3] or '-',
                    'status': row[4],
                    'application_date': row[5].isoformat() if row[5] else None,
                    'comments': row[6],
                    'created_at': row[7].isoformat() if row[7] else None
                })
            
            return {"success": True, "result": applications}
            
        except Exception as e:
            print(f"Error en get_applications_by_student: {e}")
            return {"success": True, "result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ACTUALIZAR ESTADO
    # ============================================
    def update_application_status(self, application_id: int, status: str, tutor_id: Optional[int] = None):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            if tutor_id:
                cursor.execute("""
                    UPDATE applications 
                    SET status=%s, tutor_id=%s, updated_at=%s 
                    WHERE id=%s
                """, (status, tutor_id, now, application_id))
            else:
                cursor.execute("""
                    UPDATE applications 
                    SET status=%s, updated_at=%s 
                    WHERE id=%s
                """, (status, now, application_id))
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Postulación no encontrada")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {"success": True, "message": f"Postulación {status} correctamente"}
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
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
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Postulación no encontrada")
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {"success": True, "message": "Postulación eliminada correctamente"}
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER POSTULACIÓN POR ID
    # ============================================
    def get_application_by_id(self, application_id: int):
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
                WHERE a.id = %s
            """, (application_id,))
            
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if not row:
                raise HTTPException(status_code=404, detail="Postulación no encontrada")
            
            return {
                "success": True,
                "result": {
                    'id': row[0],
                    'offer_id': row[1],
                    'offer_title': row[10] if len(row) > 10 else 'Sin título',
                    'student_id': row[2],
                    'student_name': f"{row[11]} {row[12]}" if len(row) > 12 and row[11] else 'No especificado',
                    'empresa_id': row[3],
                    'empresa_name': row[13] if len(row) > 13 else '-',
                    'tutor_id': row[4],
                    'status': row[5],
                    'application_date': row[6].isoformat() if row[6] else None,
                    'comments': row[7],
                    'created_at': row[8].isoformat() if row[8] else None
                }
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()