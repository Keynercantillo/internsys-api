import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.agreement_model import Agreement
from fastapi.encoders import jsonable_encoder

class AgreementsController:
        
    def create_agreement(self, agreement: Agreement):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO agreements (company_name, start_date, end_date, status) VALUES (%s, %s, %s, %s)", (agreement.company_name, agreement.start_date, agreement.end_date, agreement.status))
            conn.commit()
            conn.close()
            return {"result": "Agreement created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_agreement(self, agreement_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, start_date, end_date, status FROM agreements WHERE id = %s", (agreement_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Agreement not found")  

            content={
                    'id':int(result[0]),
                    'company_name':result[1],
                    'start_date':result[2],
                    'end_date':result[3],
                    'status':result[4]
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
       
    def get_agreements(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, start_date, end_date, status FROM agreements")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'company_name':data[1],
                    'start_date':data[2],
                    'end_date':data[3],
                    'status':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Agreements not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_agreements_by_company(self, company_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, start_date, end_date, status FROM agreements WHERE company_name = %s", (company_name,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'company_name':data[1],
                    'start_date':data[2],
                    'end_date':data[3],
                    'status':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No agreements found for this company")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_active_agreements(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, start_date, end_date, status FROM agreements WHERE status = 'active'")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'company_name':data[1],
                    'start_date':data[2],
                    'end_date':data[3],
                    'status':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No active agreements found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_agreement(self, agreement_id: int, agreement: Agreement):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE agreements SET company_name=%s, start_date=%s, end_date=%s, status=%s WHERE id=%s",
                (agreement.company_name, agreement.start_date, agreement.end_date, agreement.status, agreement_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Agreement not found")
            conn.commit()
            return {"result": "Agreement updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_agreement(self, agreement_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM agreements WHERE id = %s", (agreement_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Agreement not found")
            conn.commit()
            return {"result": "Agreement deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass