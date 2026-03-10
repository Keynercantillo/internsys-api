import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.internship_offer_model import InternshipOffer
from fastapi.encoders import jsonable_encoder

class InternshipOffersController:
        
    def create_offer(self, offer: InternshipOffer):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO internship_offers (offer_title, company_name, description) VALUES (%s, %s, %s)", (offer.offer_title, offer.company_name, offer.description))
            conn.commit()
            conn.close()
            return {"result": "Internship offer created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_offer(self, offer_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, offer_title, company_name, description FROM internship_offers WHERE id = %s", (offer_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Offer not found")  

            content={
                    'id':int(result[0]),
                    'offer_title':result[1],
                    'company_name':result[2],
                    'description':result[3]
            }
            json_data = jsonable_encoder(content)            
            return json_data
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
       
    def get_offers(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, offer_title, company_name, description FROM internship_offers")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'offer_title':data[1],
                    'company_name':data[2],
                    'description':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Offers not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_offers_by_company(self, company_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, offer_title, company_name, description FROM internship_offers WHERE company_name = %s", (company_name,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'offer_title':data[1],
                    'company_name':data[2],
                    'description':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No offers found for this company")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_offer(self, offer_id: int, offer: InternshipOffer):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE internship_offers SET offer_title=%s, company_name=%s, description=%s WHERE id=%s",
                (offer.offer_title, offer.company_name, offer.description, offer_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Offer not found")
            conn.commit()
            return {"result": "Offer updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_offer(self, offer_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM internship_offers WHERE id = %s", (offer_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Offer not found")
            conn.commit()
            return {"result": "Offer deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass