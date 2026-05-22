import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.offer_model import InternshipOffer
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class OffersController:
    
    # ============================================
    # CREAR OFERTA
    # ============================================
    def create_offer(self, offer: InternshipOffer):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute("""
                INSERT INTO internship_offers 
                (company_id, title, description, available_positions, required_skills, 
                 requirements, start_date, end_date, status, created_by, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                offer.company_id, offer.title, offer.description, offer.available_positions,
                offer.required_skills, offer.requirements, offer.start_date, offer.end_date,
                offer.status, offer.created_by, now, now
            ))
            
            new_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            
            return {
                "success": True,
                "result": "Offer created successfully",
                "id": new_id
            }
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            print(f"❌ Error en create_offer: {err}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER TODAS LAS OFERTAS
    # ============================================
    def get_offers(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT o.id, o.company_id, c.name as company_name, o.title, o.description, 
                       o.available_positions, o.required_skills, o.requirements, 
                       o.start_date, o.end_date, o.status, o.created_by, o.created_at, o.updated_at
                FROM internship_offers o
                LEFT JOIN companies c ON o.company_id = c.id
                ORDER BY o.created_at DESC
            """)
            
            result = cursor.fetchall()
            conn.close()
            
            payload = []
            for data in result:
                # Contar cuántas postulaciones tiene esta oferta
                postulaciones_count = self._count_applications_by_offer(data[0])
                
                payload.append({
                    'id': data[0],
                    'company_id': data[1],
                    'company_name': data[2] or 'No especificada',
                    'title': data[3],
                    'description': data[4],
                    'available_positions': data[5],
                    'required_skills': data[6],
                    'requirements': data[7],
                    'start_date': data[8].isoformat() if data[8] else None,
                    'end_date': data[9].isoformat() if data[9] else None,
                    'status': data[10],
                    'created_by': data[11],
                    'created_at': data[12].isoformat() if data[12] else None,
                    'updated_at': data[13].isoformat() if data[13] else None,
                    'applications_count': postulaciones_count
                })
            
            return {"result": jsonable_encoder(payload)}
            
        except Exception as e:
            print(f"❌ Error en get_offers: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER OFERTA POR ID
    # ============================================
    def get_offer_by_id(self, offer_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT o.id, o.company_id, c.name as company_name, o.title, o.description, 
                       o.available_positions, o.required_skills, o.requirements, 
                       o.start_date, o.end_date, o.status, o.created_by, o.created_at, o.updated_at
                FROM internship_offers o
                LEFT JOIN companies c ON o.company_id = c.id
                WHERE o.id = %s
            """, (offer_id,))
            
            data = cursor.fetchone()
            conn.close()
            
            if not data:
                raise HTTPException(status_code=404, detail="Offer not found")
            
            postulaciones_count = self._count_applications_by_offer(data[0])
            
            return {
                'id': data[0],
                'company_id': data[1],
                'company_name': data[2] or 'No especificada',
                'title': data[3],
                'description': data[4],
                'available_positions': data[5],
                'required_skills': data[6],
                'requirements': data[7],
                'start_date': data[8].isoformat() if data[8] else None,
                'end_date': data[9].isoformat() if data[9] else None,
                'status': data[10],
                'created_by': data[11],
                'created_at': data[12].isoformat() if data[12] else None,
                'updated_at': data[13].isoformat() if data[13] else None,
                'applications_count': postulaciones_count
            }
            
        except Exception as e:
            print(f"❌ Error en get_offer_by_id: {e}")
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER OFERTAS POR EMPRESA
    # ============================================
    def get_offers_by_company(self, company_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT o.id, o.company_id, c.name as company_name, o.title, o.description, 
                       o.available_positions, o.required_skills, o.requirements, 
                       o.start_date, o.end_date, o.status, o.created_by, o.created_at, o.updated_at
                FROM internship_offers o
                LEFT JOIN companies c ON o.company_id = c.id
                WHERE o.company_id = %s
                ORDER BY o.created_at DESC
            """, (company_id,))
            
            result = cursor.fetchall()
            conn.close()
            
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'company_id': data[1],
                    'company_name': data[2] or 'No especificada',
                    'title': data[3],
                    'description': data[4],
                    'available_positions': data[5],
                    'required_skills': data[6],
                    'requirements': data[7],
                    'start_date': data[8].isoformat() if data[8] else None,
                    'end_date': data[9].isoformat() if data[9] else None,
                    'status': data[10],
                    'created_by': data[11],
                    'created_at': data[12].isoformat() if data[12] else None,
                    'updated_at': data[13].isoformat() if data[13] else None
                })
            
            return {"result": jsonable_encoder(payload)}
            
        except Exception as e:
            print(f"❌ Error en get_offers_by_company: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER OFERTAS DISPONIBLES (para estudiantes)
    # ============================================
    def get_available_offers(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT o.id, o.company_id, c.name as company_name, o.title, o.description, 
                       o.available_positions, o.required_skills, o.requirements, 
                       o.start_date, o.end_date, o.status, o.created_by, o.created_at, o.updated_at
                FROM internship_offers o
                LEFT JOIN companies c ON o.company_id = c.id
                WHERE o.status = 'disponible' AND o.available_positions > 0
                ORDER BY o.created_at DESC
            """)
            
            result = cursor.fetchall()
            conn.close()
            
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'company_id': data[1],
                    'company_name': data[2] or 'No especificada',
                    'title': data[3],
                    'description': data[4],
                    'available_positions': data[5],
                    'required_skills': data[6],
                    'requirements': data[7],
                    'start_date': data[8].isoformat() if data[8] else None,
                    'end_date': data[9].isoformat() if data[9] else None,
                    'status': data[10],
                    'created_by': data[11],
                    'created_at': data[12].isoformat() if data[12] else None,
                    'updated_at': data[13].isoformat() if data[13] else None
                })
            
            return {"result": jsonable_encoder(payload)}
            
        except Exception as e:
            print(f"❌ Error en get_available_offers: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ACTUALIZAR OFERTA
    # ============================================
    def update_offer(self, offer_id: int, offer: InternshipOffer):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute("""
                UPDATE internship_offers 
                SET company_id=%s, title=%s, description=%s, available_positions=%s, 
                    required_skills=%s, requirements=%s, start_date=%s, end_date=%s, 
                    status=%s, updated_at=%s
                WHERE id=%s
            """, (
                offer.company_id, offer.title, offer.description, offer.available_positions,
                offer.required_skills, offer.requirements, offer.start_date, offer.end_date,
                offer.status, now, offer_id
            ))
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Offer not found")
            
            conn.commit()
            conn.close()
            
            return {"success": True, "result": "Offer updated successfully"}
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            print(f"❌ Error en update_offer: {err}")
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ELIMINAR OFERTA
    # ============================================
    def delete_offer(self, offer_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM internship_offers WHERE id = %s", (offer_id,))
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Offer not found")
            
            conn.commit()
            conn.close()
            
            return {"success": True, "result": "Offer deleted successfully"}
            
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            print(f"❌ Error en delete_offer: {err}")
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # CONTAR POSTULACIONES POR OFERTA (MÉTODO PRIVADO)
    # ============================================
    def _count_applications_by_offer(self, offer_id: int) -> int:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT COUNT(*) FROM applications WHERE offer_id = %s
            """, (offer_id,))
            
            count = cursor.fetchone()[0]
            conn.close()
            return count
            
        except Exception as e:
            print(f"Error counting applications: {e}")
            return 0
        finally:
            if conn:
                conn.close()