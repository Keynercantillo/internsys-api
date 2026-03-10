import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.student_model import Student
from fastapi.encoders import jsonable_encoder

class StudentsController:
        
    def create_student(self, student: Student):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (student_name, student_id_code, major) VALUES (%s, %s, %s)", (student.student_name, student.student_id_code, student.major))
            conn.commit()
            conn.close()
            return {"result": "Student created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, student_id_code, major FROM students WHERE id = %s", (student_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Student not found")  

            content={
                    'id':int(result[0]),
                    'student_name':result[1],
                    'student_id_code':result[2],
                    'major':result[3]
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
       
    def get_students(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, student_id_code, major FROM students")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'student_id_code':data[2],
                    'major':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Students not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_student_by_code(self, student_id_code: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, student_id_code, major FROM students WHERE student_id_code = %s", (student_id_code,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Student not found")  

            content={
                    'id':int(result[0]),
                    'student_name':result[1],
                    'student_id_code':result[2],
                    'major':result[3]
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
    
    def update_student(self, student_id: int, student: Student):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE students SET student_name=%s, student_id_code=%s, major=%s WHERE id=%s",
                (student.student_name, student.student_id_code, student.major, student_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Student not found")
            conn.commit()
            return {"result": "Student updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Student not found")
            conn.commit()
            return {"result": "Student deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass