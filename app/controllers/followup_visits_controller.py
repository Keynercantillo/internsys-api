import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.followup_visit_model import FollowupVisit
from fastapi.encoders import jsonable_encoder

class FollowupVisitsController:
        
    def create_visit(self, visit: FollowupVisit):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO followup_visits (student_name, visit_date, observations) VALUES (%s, %s, %s)", (visit.student_name, visit.visit_date, visit.observations))
            conn.commit()
            conn.close()
            return {"result": "Follow-up visit created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_visit(self, visit_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, visit_date, observations FROM followup_visits WHERE id = %s", (visit_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Visit not found")  

            content={
                    'id':int(result[0]),
                    'student_name':result[1],
                    'visit_date':result[2],
                    'observations':result[3]
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
       
    def get_visits(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, visit_date, observations FROM followup_visits")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'visit_date':data[2],
                    'observations':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Visits not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_visits_by_student(self, student_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, visit_date, observations FROM followup_visits WHERE student_name = %s ORDER BY visit_date DESC", (student_name,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'visit_date':data[2],
                    'observations':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No visits found for this student")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_visit(self, visit_id: int, visit: FollowupVisit):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE followup_visits SET student_name=%s, visit_date=%s, observations=%s WHERE id=%s",
                (visit.student_name, visit.visit_date, visit.observations, visit_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Visit not found")
            conn.commit()
            return {"result": "Follow-up visit updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_visit(self, visit_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM followup_visits WHERE id = %s", (visit_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Visit not found")
            conn.commit()
            return {"result": "Follow-up visit deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass