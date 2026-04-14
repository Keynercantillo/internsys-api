import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.agreement_model import Agreement
from fastapi.encoders import jsonable_encoder

class AgreementsController:
        
    def create_agreement(self, agreement: Agreement):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO agreements (student_id, tutor_id, company_id, start_date, end_date, status, signed_date, file_url) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (agreement.student_id, agreement.tutor_id, agreement.company_id, agreement.start_date, 
                 agreement.end_date, agreement.status, agreement.signed_date, agreement.file_url)
            )
            conn.commit()
            conn.close()
            return {"result": "Agreement created"}
        except psycopg2.Error as err:
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
            cursor.execute("SELECT id, student_id, tutor_id, company_id, start_date, end_date, status, signed_date, file_url FROM agreements WHERE id = %s", (agreement_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Agreement not found")  

            content = {
                'id': int(result[0]),
                'student_id': result[1],
                'tutor_id': result[2],
                'company_id': result[3],
                'start_date': result[4],
                'end_date': result[5],
                'status': result[6],
                'signed_date': result[7],
                'file_url': result[8]
            }
            json_data = jsonable_encoder(content)            
            return json_data
        except psycopg2.Error as err:
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
            cursor.execute("SELECT id, student_id, tutor_id, company_id, start_date, end_date, status, signed_date, file_url FROM agreements")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'student_id': data[1],
                    'tutor_id': data[2],
                    'company_id': data[3],
                    'start_date': data[4],
                    'end_date': data[5],
                    'status': data[6],
                    'signed_date': data[7],
                    'file_url': data[8]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Agreements not found")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_agreements_by_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_id, tutor_id, company_id, start_date, end_date, status, signed_date, file_url FROM agreements WHERE student_id = %s", (student_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'student_id': data[1],
                    'tutor_id': data[2],
                    'company_id': data[3],
                    'start_date': data[4],
                    'end_date': data[5],
                    'status': data[6],
                    'signed_date': data[7],
                    'file_url': data[8]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No agreements found for student {student_id}")  
        except psycopg2.Error as err:
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
                """UPDATE agreements SET student_id=%s, tutor_id=%s, company_id=%s, start_date=%s, end_date=%s, 
                   status=%s, signed_date=%s, file_url=%s WHERE id=%s""",
                (agreement.student_id, agreement.tutor_id, agreement.company_id, agreement.start_date, 
                 agreement.end_date, agreement.status, agreement.signed_date, agreement.file_url, agreement_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Agreement not found")
            conn.commit()
            return {"result": "Agreement updated"}
        except psycopg2.Error as err:
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
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass