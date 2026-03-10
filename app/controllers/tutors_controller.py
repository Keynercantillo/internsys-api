import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.tutor_model import Tutor
from fastapi.encoders import jsonable_encoder

class TutorsController:
        
    def create_tutor(self, tutor: Tutor):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tutors (tutor_name, department_faculty) VALUES (%s, %s)", (tutor.tutor_name, tutor.department_faculty))
            conn.commit()
            conn.close()
            return {"result": "Tutor created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_tutor(self, tutor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, tutor_name, department_faculty FROM tutors WHERE id = %s", (tutor_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Tutor not found")  

            content={
                    'id':int(result[0]),
                    'tutor_name':result[1],
                    'department_faculty':result[2]
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
       
    def get_tutors(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, tutor_name, department_faculty FROM tutors")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'tutor_name':data[1],
                    'department_faculty':data[2]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Tutors not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_tutor_by_name(self, tutor_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, tutor_name, department_faculty FROM tutors WHERE tutor_name = %s", (tutor_name,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Tutor not found")  

            content={
                    'id':int(result[0]),
                    'tutor_name':result[1],
                    'department_faculty':result[2]
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
    
    def update_tutor(self, tutor_id: int, tutor: Tutor):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tutors SET tutor_name=%s, department_faculty=%s WHERE id=%s",
                (tutor.tutor_name, tutor.department_faculty, tutor_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tutor not found")
            conn.commit()
            return {"result": "Tutor updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_tutor(self, tutor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tutors WHERE id = %s", (tutor_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tutor not found")
            conn.commit()
            return {"result": "Tutor deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass