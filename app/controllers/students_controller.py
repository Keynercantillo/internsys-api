import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.students_model import Student
from fastapi.encoders import jsonable_encoder

class StudentsController:
    
    def create_student(self, student: Student):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO students (nombre, apellido, cedula, edad, usuario, contraseña, matricula, carrera, semester, promedio, tutor_academico_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (student.nombre, student.apellido, student.cedula, student.edad, student.usuario, 
                 student.contraseña, student.matricula, student.carrera, student.semester, student.promedio, student.tutor_academico_id)
            )
            conn.commit()
            conn.close()
            return {"result": "Student created successfully"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_students(self):
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, matricula, carrera, semester, promedio, tutor_academico_id FROM students")
            result = cursor.fetchall()
            
            if not result:
                return {"result": []}
            
            payload = []
            for data in result:
                payload.append({
                    'id': data[0],
                    'nombre': data[1],
                    'apellido': data[2],
                    'cedula': data[3],
                    'edad': data[4],
                    'usuario': data[5],
                    'contraseña': data[6],
                    'matricula': data[7],
                    'carrera': data[8],
                    'semester': data[9],
                    'promedio': data[10],
                    'tutor_academico_id': data[11]
                })
            
            return {"result": jsonable_encoder(payload)}
            
        except psycopg2.Error as err:
            print(f"Error en get_students: {err}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        except Exception as err:
            print(f"Error inesperado: {err}")
            raise HTTPException(status_code=500, detail=f"Error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    def get_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, matricula, carrera, semester, promedio, tutor_academico_id FROM students WHERE id = %s", (student_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Student not found")
            
            content = {
                'id': result[0],
                'nombre': result[1],
                'apellido': result[2],
                'cedula': result[3],
                'edad': result[4],
                'usuario': result[5],
                'contraseña': result[6],
                'matricula': result[7],
                'carrera': result[8],
                'semester': result[9],
                'promedio': result[10],
                'tutor_academico_id': result[11]
            }
            return jsonable_encoder(content)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            conn.close()
    
    def get_students_by_career(self, carrera: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, matricula, carrera, semester, promedio, tutor_academico_id FROM students WHERE carrera = %s", (carrera,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                payload.append({
                    'id': data[0], 'nombre': data[1], 'apellido': data[2], 'cedula': data[3],
                    'edad': data[4], 'usuario': data[5], 'contraseña': data[6], 'matricula': data[7],
                    'carrera': data[8], 'semester': data[9], 'promedio': data[10], 'tutor_academico_id': data[11]
                })
            return {"result": jsonable_encoder(payload)}
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            conn.close()
    
    def update_student(self, student_id: int, student: Student):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE students SET nombre=%s, apellido=%s, cedula=%s, edad=%s, usuario=%s, contraseña=%s, 
                   matricula=%s, carrera=%s, semester=%s, promedio=%s, tutor_academico_id=%s WHERE id=%s""",
                (student.nombre, student.apellido, student.cedula, student.edad, student.usuario, student.contraseña,
                 student.matricula, student.carrera, student.semester, student.promedio, student.tutor_academico_id, student_id),
            )
            conn.commit()
            return {"result": "Student updated successfully"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            conn.close()

    def delete_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            return {"result": "Student deleted successfully"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            conn.close()