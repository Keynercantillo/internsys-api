import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.students_model import Student
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class StudentsController:
    
    # ============================================
    # CREAR ESTUDIANTE
    # ============================================
    def create_student(self, student: Student):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute(
                """INSERT INTO students (nombre, apellido, cedula, edad, usuario, contraseña, matricula, carrera, semester, promedio, tutor_academico_id, created_at, updated_at) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (student.nombre, student.apellido, student.cedula, student.edad, student.usuario, 
                 student.contraseña, student.matricula, student.carrera, student.semester, 
                 student.promedio, student.tutor_academico_id, now, now)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return {"result": "Student created successfully", "id": new_id, "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER ESTUDIANTE POR ID
    # ============================================
    def get_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, matricula, carrera, semester, promedio, tutor_academico_id, created_at, updated_at FROM students WHERE id = %s", 
                (student_id,)
            )
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Student not found")  

            content = {
                'id': int(result[0]),
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
                'tutor_academico_id': result[11],
                'created_at': result[12],
                'updated_at': result[13]
            }
            return jsonable_encoder(content)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER TODOS LOS ESTUDIANTES
    # ============================================
    def get_students(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, matricula, carrera, semester, promedio, tutor_academico_id, created_at, updated_at FROM students ORDER BY id DESC")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
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
                    'tutor_academico_id': data[11],
                    'created_at': data[12],
                    'updated_at': data[13]
                }
                payload.append(content)
            return {"result": jsonable_encoder(payload)} if payload else {"result": []}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER ESTUDIANTES POR CARRERA
    # ============================================
    def get_students_by_career(self, carrera: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, 
                       matricula, carrera, semester, promedio, tutor_academico_id, 
                       created_at, updated_at 
                FROM students WHERE carrera = %s
            """, (carrera,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'nombre': data[1], 'apellido': data[2], 'cedula': data[3],
                    'edad': data[4], 'usuario': data[5], 'contraseña': data[6], 'matricula': data[7],
                    'carrera': data[8], 'semester': data[9], 'promedio': data[10], 
                    'tutor_academico_id': data[11], 'created_at': data[12], 'updated_at': data[13]
                }
                payload.append(content)
            return {"result": jsonable_encoder(payload)} if payload else {"result": []}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ACTUALIZAR ESTUDIANTE
    # ============================================
    def update_student(self, student_id: int, student: Student):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute(
                """UPDATE students 
                   SET nombre=%s, apellido=%s, cedula=%s, edad=%s, usuario=%s, contraseña=%s, 
                       matricula=%s, carrera=%s, semester=%s, promedio=%s, tutor_academico_id=%s, updated_at=%s 
                   WHERE id=%s""",
                (student.nombre, student.apellido, student.cedula, student.edad, student.usuario, 
                 student.contraseña, student.matricula, student.carrera, student.semester, 
                 student.promedio, student.tutor_academico_id, now, student_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Student not found")
            conn.commit()
            return {"result": "Student updated successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()

    # ============================================
    # ELIMINAR ESTUDIANTE
    # ============================================
    def delete_student(self, student_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Student not found")
            conn.commit()
            return {"result": "Student deleted successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()