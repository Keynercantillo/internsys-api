import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.internship_offers_model import InternshipOffer
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class InternshipOfferController:
    
    # ============================================
    # CREAR OFERTA
    # ============================================
    def create_offer(self, offer: InternshipOffer):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute(
                """INSERT INTO internship_offers (company_id, title, description, required_skills, available_positions, start_date, end_date, status, requirements, created_at, updated_at) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (offer.company_id, offer.title, offer.description, offer.required_skills, offer.available_positions,
                 offer.start_date, offer.end_date, offer.status, offer.requirements, now, now)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return {"result": "Offer created successfully", "id": new_id, "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER OFERTA POR ID
    # ============================================
    def get_offer(self, offer_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, company_id, title, description, required_skills, available_positions, start_date, end_date, status, requirements, created_at, updated_at FROM internship_offers WHERE id = %s", 
                (offer_id,)
            )
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Offer not found")  

            content = {
                'id': int(result[0]),
                'company_id': result[1],
                'title': result[2],
                'description': result[3],
                'required_skills': result[4],
                'available_positions': result[5],
                'start_date': result[6],
                'end_date': result[7],
                'status': result[8],
                'requirements': result[9],
                'created_at': result[10],
                'updated_at': result[11]
            }
            return jsonable_encoder(content)
        except psycopg2.Error as err:
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
            cursor.execute("SELECT id, company_id, title, description, required_skills, available_positions, start_date, end_date, status, requirements, created_at, updated_at FROM internship_offers ORDER BY id DESC")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'company_id': data[1], 'title': data[2], 'description': data[3],
                    'required_skills': data[4], 'available_positions': data[5], 'start_date': data[6],
                    'end_date': data[7], 'status': data[8], 'requirements': data[9],
                    'created_at': data[10], 'updated_at': data[11]
                }
                payload.append(content)
            return {"result": jsonable_encoder(payload)} if payload else {"result": []}
        except Exception as e:
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
                SELECT id, company_id, title, description, required_skills, available_positions, 
                       start_date, end_date, status, requirements, created_at, updated_at 
                FROM internship_offers WHERE company_id = %s
                ORDER BY id DESC
            """, (company_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'company_id': data[1], 'title': data[2], 'description': data[3],
                    'required_skills': data[4], 'available_positions': data[5], 'start_date': data[6],
                    'end_date': data[7], 'status': data[8], 'requirements': data[9],
                    'created_at': data[10], 'updated_at': data[11]
                }
                payload.append(content)
            return {"result": jsonable_encoder(payload)} if payload else {"result": []}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
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
            
            cursor.execute(
                """UPDATE internship_offers 
                   SET company_id=%s, title=%s, description=%s, required_skills=%s, 
                       available_positions=%s, start_date=%s, end_date=%s, status=%s, 
                       requirements=%s, updated_at=%s 
                   WHERE id=%s""",
                (offer.company_id, offer.title, offer.description, offer.required_skills, offer.available_positions,
                 offer.start_date, offer.end_date, offer.status, offer.requirements, now, offer_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Offer not found")
            conn.commit()
            return {"result": "Offer updated successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
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
            return {"result": "Offer deleted successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()