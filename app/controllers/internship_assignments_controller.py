import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.internship_assignment_model import InternshipAssignment
from fastapi.encoders import jsonable_encoder

class InternshipAssignmentsController:
        
    def create_assignment(self, assignment: InternshipAssignment):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO internship_assignments (student_name, offer_title, tutor_name, process_status) VALUES (%s, %s, %s, %s)", (assignment.student_name, assignment.offer_title, assignment.tutor_name, assignment.process_status))
            conn.commit()
            conn.close()
            return {"result": "Internship assignment created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_assignment(self, assignment_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, offer_title, tutor_name, process_status FROM internship_assignments WHERE id = %s", (assignment_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Assignment not found")  

            content={
                    'id':int(result[0]),
                    'student_name':result[1],
                    'offer_title':result[2],
                    'tutor_name':result[3],
                    'process_status':result[4]
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
       
    def get_assignments(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, offer_title, tutor_name, process_status FROM internship_assignments")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'offer_title':data[2],
                    'tutor_name':data[3],
                    'process_status':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Assignments not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_assignments_by_student(self, student_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, offer_title, tutor_name, process_status FROM internship_assignments WHERE student_name = %s", (student_name,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'offer_title':data[2],
                    'tutor_name':data[3],
                    'process_status':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No assignments found for this student")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_assignments_by_tutor(self, tutor_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, offer_title, tutor_name, process_status FROM internship_assignments WHERE tutor_name = %s", (tutor_name,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'offer_title':data[2],
                    'tutor_name':data[3],
                    'process_status':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No assignments found for this tutor")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_assignments_by_offer(self, offer_title: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, offer_title, tutor_name, process_status FROM internship_assignments WHERE offer_title = %s", (offer_title,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'offer_title':data[2],
                    'tutor_name':data[3],
                    'process_status':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No assignments found for this offer")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_assignment(self, assignment_id: int, assignment: InternshipAssignment):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE internship_assignments SET student_name=%s, offer_title=%s, tutor_name=%s, process_status=%s WHERE id=%s",
                (assignment.student_name, assignment.offer_title, assignment.tutor_name, assignment.process_status, assignment_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Assignment not found")
            conn.commit()
            return {"result": "Assignment updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_assignment(self, assignment_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM internship_assignments WHERE id = %s", (assignment_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Assignment not found")
            conn.commit()
            return {"result": "Assignment deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass