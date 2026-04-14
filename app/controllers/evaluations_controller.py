import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.evaluation_model import Evaluation
from fastapi.encoders import jsonable_encoder

class EvaluationsController:
        
    def create_evaluation(self, evaluation: Evaluation):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO evaluations (internship_assignment_id, evaluator_id, evaluation_type, score, comments, evaluation_date, criteria_json) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (evaluation.internship_assignment_id, evaluation.evaluator_id, evaluation.evaluation_type, 
                 evaluation.score, evaluation.comments, evaluation.evaluation_date, evaluation.criteria_json)
            )
            conn.commit()
            conn.close()
            return {"result": "Evaluation created"}
        except psycopg2.Error as err:
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
            cursor.execute("SELECT id, internship_assignment_id, evaluator_id, evaluation_type, score, comments, evaluation_date, criteria_json FROM evaluations WHERE id = %s", (evaluation_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Evaluation not found")  

            content = {
                'id': int(result[0]),
                'internship_assignment_id': result[1],
                'evaluator_id': result[2],
                'evaluation_type': result[3],
                'score': result[4],
                'comments': result[5],
                'evaluation_date': result[6],
                'criteria_json': result[7]
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
       
    def get_evaluations(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, internship_assignment_id, evaluator_id, evaluation_type, score, comments, evaluation_date, criteria_json FROM evaluations")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'internship_assignment_id': data[1],
                    'evaluator_id': data[2],
                    'evaluation_type': data[3],
                    'score': data[4],
                    'comments': data[5],
                    'evaluation_date': data[6],
                    'criteria_json': data[7]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Evaluations not found")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_evaluations_by_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.internship_assignment_id, e.evaluator_id, e.evaluation_type, e.score, e.comments, e.evaluation_date, e.criteria_json 
                FROM evaluations e
                JOIN internship_assignments ia ON e.internship_assignment_id = ia.id
                WHERE ia.student_id = %s
            """, (student_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'internship_assignment_id': data[1],
                    'evaluator_id': data[2],
                    'evaluation_type': data[3],
                    'score': data[4],
                    'comments': data[5],
                    'evaluation_date': data[6],
                    'criteria_json': data[7]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No evaluations found for student {student_id}")  
        except psycopg2.Error as err:
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
                """UPDATE evaluations SET internship_assignment_id=%s, evaluator_id=%s, evaluation_type=%s, 
                   score=%s, comments=%s, evaluation_date=%s, criteria_json=%s WHERE id=%s""",
                (evaluation.internship_assignment_id, evaluation.evaluator_id, evaluation.evaluation_type,
                 evaluation.score, evaluation.comments, evaluation.evaluation_date, evaluation.criteria_json, evaluation_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Evaluation not found")
            conn.commit()
            return {"result": "Evaluation updated"}
        except psycopg2.Error as err:
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
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass