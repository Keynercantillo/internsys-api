import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.followup_visit_model import FollowupVisit
from fastapi.encoders import jsonable_encoder

class FollowupVisitsController:
        
    def create_followup_visit(self, followup_visit: FollowupVisit):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO followup_visits (internship_assignment_id, visit_date, tutor_feedback, student_feedback, supervisor_name, observations, status, next_visit_date) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (followup_visit.internship_assignment_id, followup_visit.visit_date, followup_visit.tutor_feedback,
                 followup_visit.student_feedback, followup_visit.supervisor_name, followup_visit.observations,
                 followup_visit.status, followup_visit.next_visit_date)
            )
            conn.commit()
            conn.close()
            return {"result": "Follow-up visit created"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        
    def get_followup_visit(self, visit_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, internship_assignment_id, visit_date, tutor_feedback, student_feedback, supervisor_name, observations, status, next_visit_date FROM followup_visits WHERE id = %s", (visit_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Follow-up visit not found")  

            content = {
                'id': int(result[0]),
                'internship_assignment_id': result[1],
                'visit_date': result[2],
                'tutor_feedback': result[3],
                'student_feedback': result[4],
                'supervisor_name': result[5],
                'observations': result[6],
                'status': result[7],
                'next_visit_date': result[8]
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
       
    def get_followup_visits(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, internship_assignment_id, visit_date, tutor_feedback, student_feedback, supervisor_name, observations, status, next_visit_date FROM followup_visits")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'internship_assignment_id': data[1],
                    'visit_date': data[2],
                    'tutor_feedback': data[3],
                    'student_feedback': data[4],
                    'supervisor_name': data[5],
                    'observations': data[6],
                    'status': data[7],
                    'next_visit_date': data[8]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Follow-up visits not found")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_visits_by_assignment(self, assignment_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, internship_assignment_id, visit_date, tutor_feedback, student_feedback, supervisor_name, observations, status, next_visit_date FROM followup_visits WHERE internship_assignment_id = %s", (assignment_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'internship_assignment_id': data[1],
                    'visit_date': data[2],
                    'tutor_feedback': data[3],
                    'student_feedback': data[4],
                    'supervisor_name': data[5],
                    'observations': data[6],
                    'status': data[7],
                    'next_visit_date': data[8]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No visits found for assignment {assignment_id}")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_followup_visit(self, visit_id: int, followup_visit: FollowupVisit):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE followup_visits SET internship_assignment_id=%s, visit_date=%s, tutor_feedback=%s, 
                   student_feedback=%s, supervisor_name=%s, observations=%s, status=%s, next_visit_date=%s WHERE id=%s""",
                (followup_visit.internship_assignment_id, followup_visit.visit_date, followup_visit.tutor_feedback,
                 followup_visit.student_feedback, followup_visit.supervisor_name, followup_visit.observations,
                 followup_visit.status, followup_visit.next_visit_date, visit_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Follow-up visit not found")
            conn.commit()
            return {"result": "Follow-up visit updated"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_followup_visit(self, visit_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM followup_visits WHERE id = %s", (visit_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Follow-up visit not found")
            conn.commit()
            return {"result": "Follow-up visit deleted"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass