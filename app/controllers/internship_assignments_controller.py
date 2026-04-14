import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.internship_assignments_model import InternshipAssignment
from fastapi.encoders import jsonable_encoder

class InternshipAssignmentController:
    
    def create_assignment(self, assignment: InternshipAssignment):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO internship_assignments (student_id, internship_offer_id, tutor_id, assignment_date, start_date, end_date, status, schedule, total_hours, completed_hours) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (assignment.student_id, assignment.internship_offer_id, assignment.tutor_id, assignment.assignment_date,
                 assignment.start_date, assignment.end_date, assignment.status, assignment.schedule, 
                 assignment.total_hours, assignment.completed_hours)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return {"result": "Assignment created successfully", "id": new_id}
        except psycopg2.Error as err:
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
            cursor.execute("""
                SELECT 
                    a.id, a.student_id, s.nombre as student_nombre, s.apellido as student_apellido,
                    a.internship_offer_id, o.title as offer_title,
                    a.tutor_id, t.nombre as tutor_nombre, t.apellido as tutor_apellido,
                    a.assignment_date, a.start_date, a.end_date, a.status, a.schedule, a.total_hours, a.completed_hours
                FROM internship_assignments a
                LEFT JOIN students s ON a.student_id = s.id
                LEFT JOIN internship_offers o ON a.internship_offer_id = o.id
                LEFT JOIN tutors t ON a.tutor_id = t.id
                WHERE a.id = %s
            """, (assignment_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Assignment not found")
            
            content = {
                'id': result[0],
                'student_id': result[1],
                'student_nombre': f"{result[2]} {result[3]}" if result[2] else 'No asignado',
                'internship_offer_id': result[4],
                'offer_title': result[5] or 'Sin título',
                'tutor_id': result[6],
                'tutor_nombre': f"{result[7]} {result[8]}" if result[7] else 'No asignado',
                'assignment_date': result[9],
                'start_date': result[10],
                'end_date': result[11],
                'status': result[12] or 'activo',
                'schedule': result[13],
                'total_hours': result[14],
                'completed_hours': result[15]
            }
            conn.close()
            return jsonable_encoder(content)
        except psycopg2.Error as err:
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
            cursor.execute("""
                SELECT 
                    a.id,
                    a.student_id,
                    s.nombre as student_nombre,
                    s.apellido as student_apellido,
                    a.internship_offer_id,
                    o.title as offer_title,
                    a.tutor_id,
                    t.nombre as tutor_nombre,
                    t.apellido as tutor_apellido,
                    a.assignment_date,
                    a.start_date,
                    a.end_date,
                    a.status,
                    a.schedule,
                    a.total_hours,
                    a.completed_hours
                FROM internship_assignments a
                LEFT JOIN students s ON a.student_id = s.id
                LEFT JOIN internship_offers o ON a.internship_offer_id = o.id
                LEFT JOIN tutors t ON a.tutor_id = t.id
                ORDER BY a.id DESC
            """)
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'student_id': data[1],
                    'student_nombre': f"{data[2]} {data[3]}" if data[2] else 'No asignado',
                    'internship_offer_id': data[4],
                    'offer_title': data[5] or 'Sin título',
                    'tutor_id': data[6],
                    'tutor_nombre': f"{data[7]} {data[8]}" if data[7] else 'No asignado',
                    'assignment_date': data[9],
                    'start_date': data[10],
                    'end_date': data[11],
                    'status': data[12] or 'activo',
                    'schedule': data[13],
                    'total_hours': data[14],
                    'completed_hours': data[15]
                }
                payload.append(content)
            conn.close()
            return {"result": jsonable_encoder(payload)}
        except Exception as e:
            print(f"Error en get_assignments: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    def get_assignments_by_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    a.id,
                    a.student_id,
                    s.nombre as student_nombre,
                    s.apellido as student_apellido,
                    a.internship_offer_id,
                    o.title as offer_title,
                    a.tutor_id,
                    t.nombre as tutor_nombre,
                    t.apellido as tutor_apellido,
                    a.assignment_date,
                    a.start_date,
                    a.end_date,
                    a.status,
                    a.schedule,
                    a.total_hours,
                    a.completed_hours
                FROM internship_assignments a
                LEFT JOIN students s ON a.student_id = s.id
                LEFT JOIN internship_offers o ON a.internship_offer_id = o.id
                LEFT JOIN tutors t ON a.tutor_id = t.id
                WHERE a.student_id = %s
                ORDER BY a.id DESC
            """, (student_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'student_id': data[1],
                    'student_nombre': f"{data[2]} {data[3]}" if data[2] else 'No asignado',
                    'internship_offer_id': data[4],
                    'offer_title': data[5] or 'Sin título',
                    'tutor_id': data[6],
                    'tutor_nombre': f"{data[7]} {data[8]}" if data[7] else 'No asignado',
                    'assignment_date': data[9],
                    'start_date': data[10],
                    'end_date': data[11],
                    'status': data[12] or 'activo',
                    'schedule': data[13],
                    'total_hours': data[14],
                    'completed_hours': data[15]
                }
                payload.append(content)
            conn.close()
            return {"result": jsonable_encoder(payload)}
        except Exception as e:
            print(f"Error en get_assignments_by_student: {e}")
            return {"result": []}
        finally:
            if conn:
                conn.close()
    
    def update_assignment(self, assignment_id: int, assignment: InternshipAssignment):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE internship_assignments 
                   SET student_id=%s, internship_offer_id=%s, tutor_id=%s, 
                       assignment_date=%s, start_date=%s, end_date=%s, status=%s, 
                       schedule=%s, total_hours=%s, completed_hours=%s 
                   WHERE id=%s""",
                (assignment.student_id, assignment.internship_offer_id, assignment.tutor_id, 
                 assignment.assignment_date, assignment.start_date, assignment.end_date, 
                 assignment.status, assignment.schedule, assignment.total_hours, 
                 assignment.completed_hours, assignment_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Assignment not found")
            conn.commit()
            return {"result": "Assignment updated successfully"}
        except psycopg2.Error as err:
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
            return {"result": "Assignment deleted successfully"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass