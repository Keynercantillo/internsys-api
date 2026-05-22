import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.evaluation_model import Evaluation
from fastapi.encoders import jsonable_encoder

class EvaluationsController:
    
    def create_evaluation(self, evaluation: Evaluation):   
        """Crear una nueva evaluación (solo tutores asignados)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar que el tutor esté asignado al estudiante
            cursor.execute("""
                SELECT ia.id FROM internship_assignments ia
                WHERE ia.id = %s AND ia.tutor_id = %s
            """, (evaluation.internship_assignment_id, evaluation.evaluator_id))
            
            if not cursor.fetchone():
                raise HTTPException(status_code=403, detail="No tienes permiso para evaluar este estudiante")
            
            cursor.execute(
                """INSERT INTO evaluations (internship_assignment_id, evaluator_id, evaluation_type, 
                   score, comments, evaluation_date, criteria_json) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (evaluation.internship_assignment_id, evaluation.evaluator_id, evaluation.evaluation_type, 
                 evaluation.score, evaluation.comments, evaluation.evaluation_date, evaluation.criteria_json)
            )
            conn.commit()
            return {"result": "Evaluation created", "id": cursor.lastrowid}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        
    def get_evaluations_by_tutor(self, tutor_id: int):
        """Obtener todas las evaluaciones hechas por un tutor"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.internship_assignment_id, e.evaluator_id, e.evaluation_type, 
                       e.score, e.comments, e.evaluation_date, e.criteria_json,
                       s.id as student_id, s.nombre as student_name, s.apellido as student_apellido,
                       ia.student_id
                FROM evaluations e
                JOIN internship_assignments ia ON e.internship_assignment_id = ia.id
                JOIN students s ON ia.student_id = s.id
                WHERE e.evaluator_id = %s
                ORDER BY e.evaluation_date DESC
            """, (tutor_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'internship_assignment_id': data[1],
                    'student_id': data[8],
                    'student_name': f"{data[9]} {data[10]}",
                    'evaluation_type': data[3],
                    'score': float(data[4]) if data[4] else None,
                    'comments': data[5],
                    'evaluation_date': data[6].isoformat() if data[6] else None,
                    'status': 'completed' if data[4] is not None else 'pending'
                }
                payload.append(content)
            return {"result": payload}
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_evaluations_by_student_and_tutor(self, student_id: int, tutor_id: int):
        """Obtener evaluaciones de un estudiante por un tutor específico"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.internship_assignment_id, e.evaluation_type, 
                       e.score, e.comments, e.evaluation_date
                FROM evaluations e
                JOIN internship_assignments ia ON e.internship_assignment_id = ia.id
                WHERE ia.student_id = %s AND e.evaluator_id = %s
                ORDER BY e.evaluation_date DESC
            """, (student_id, tutor_id))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'internship_assignment_id': data[1],
                    'evaluation_type': data[2],
                    'score': float(data[3]) if data[3] else None,
                    'comments': data[4],
                    'evaluation_date': data[5].isoformat() if data[5] else None,
                }
                payload.append(content)
            return {"result": payload}
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_evaluation(self, evaluation_id: int, evaluation: Evaluation, tutor_id: int):
        """Actualizar una evaluación (solo el tutor que la creó)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Verificar que la evaluación pertenece al tutor
            cursor.execute(
                "SELECT id FROM evaluations WHERE id = %s AND evaluator_id = %s",
                (evaluation_id, tutor_id)
            )
            if not cursor.fetchone():
                raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta evaluación")
            
            cursor.execute(
                """UPDATE evaluations SET evaluation_type=%s, score=%s, comments=%s, 
                   evaluation_date=%s, criteria_json=%s WHERE id=%s""",
                (evaluation.evaluation_type, evaluation.score, evaluation.comments,
                 evaluation.evaluation_date, evaluation.criteria_json, evaluation_id),
            )
            conn.commit()
            return {"result": "Evaluation updated"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_evaluation(self, evaluation_id: int, tutor_id: int):
        """Eliminar una evaluación (solo el tutor que la creó)"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "DELETE FROM evaluations WHERE id = %s AND evaluator_id = %s",
                (evaluation_id, tutor_id)
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta evaluación")
            conn.commit()
            return {"result": "Evaluation deleted"}
        except HTTPException:
            raise
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass