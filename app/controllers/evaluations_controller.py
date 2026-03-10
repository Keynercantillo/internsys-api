import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.evaluation_model import Evaluation
from fastapi.encoders import jsonable_encoder

class EvaluationsController:
        
    def create_evaluation(self, evaluation: Evaluation):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO evaluations (student_name, score, comments) VALUES (%s, %s, %s)", (evaluation.student_name, evaluation.score, evaluation.comments))
            conn.commit()
            conn.close()
            return {"result": "Evaluation created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_evaluation(self, evaluation_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, score, comments FROM evaluations WHERE id = %s", (evaluation_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Evaluation not found")  

            content={
                    'id':int(result[0]),
                    'student_name':result[1],
                    'score':float(result[2]) if result[2] else None,
                    'comments':result[3]
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
       
    def get_evaluations(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, score, comments FROM evaluations")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'score':data[2],
                    'comments':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Evaluations not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_evaluations_by_student(self, student_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, score, comments FROM evaluations WHERE student_name = %s", (student_name,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'score':data[2],
                    'comments':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No evaluations found for this student")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_evaluation(self, evaluation_id: int, evaluation: Evaluation):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE evaluations SET student_name=%s, score=%s, comments=%s WHERE id=%s",
                (evaluation.student_name, evaluation.score, evaluation.comments, evaluation_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Evaluation not found")
            conn.commit()
            return {"result": "Evaluation updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_evaluation(self, evaluation_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM evaluations WHERE id = %s", (evaluation_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Evaluation not found")
            conn.commit()
            return {"result": "Evaluation deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass