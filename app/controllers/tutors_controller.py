import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.tutor_model import Tutor
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class TutorsController:
    
    # ============================================
    # CREAR TUTOR
    # ============================================
    def create_tutor(self, tutor: Tutor):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute(
                """INSERT INTO tutors (nombre, apellido, cedula, edad, usuario, contraseña, tipo, especialidad, telefono, email, empresa_id, created_at, updated_at) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (tutor.nombre, tutor.apellido, tutor.cedula, tutor.edad, tutor.usuario, tutor.contraseña,
                 tutor.tipo, tutor.especialidad, tutor.telefono, tutor.email, tutor.empresa_id, now, now)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return {"result": "Tutor created successfully", "id": new_id, "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER TUTOR POR ID
    # ============================================
    def get_tutor(self, tutor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, tipo, especialidad, telefono, email, empresa_id, created_at, updated_at FROM tutors WHERE id = %s", 
                (tutor_id,)
            )
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Tutor not found")  

            content = {
                'id': int(result[0]),
                'nombre': result[1],
                'apellido': result[2],
                'cedula': result[3],
                'edad': result[4],
                'usuario': result[5],
                'contraseña': result[6],
                'tipo': result[7],
                'especialidad': result[8],
                'telefono': result[9],
                'email': result[10],
                'empresa_id': result[11],
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
    # OBTENER TODOS LOS TUTORES
    # ============================================
    def get_tutors(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, tipo, especialidad, telefono, email, empresa_id, created_at, updated_at FROM tutors ORDER BY id DESC")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'nombre': data[1], 'apellido': data[2], 'cedula': data[3],
                    'edad': data[4], 'usuario': data[5], 'contraseña': data[6], 'tipo': data[7],
                    'especialidad': data[8], 'telefono': data[9], 'email': data[10], 
                    'empresa_id': data[11], 'created_at': data[12], 'updated_at': data[13]
                }
                payload.append(content)
            return {"result": jsonable_encoder(payload)} if payload else {"result": []}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # OBTENER TUTORES POR TIPO
    # ============================================
    def get_tutors_by_type(self, tipo: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, tipo, 
                       especialidad, telefono, email, empresa_id, created_at, updated_at 
                FROM tutors WHERE tipo = %s
            """, (tipo,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'nombre': data[1], 'apellido': data[2], 'cedula': data[3],
                    'edad': data[4], 'usuario': data[5], 'contraseña': data[6], 'tipo': data[7],
                    'especialidad': data[8], 'telefono': data[9], 'email': data[10], 
                    'empresa_id': data[11], 'created_at': data[12], 'updated_at': data[13]
                }
                payload.append(content)
            return {"result": jsonable_encoder(payload)} if payload else {"result": []}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            if conn:
                conn.close()
    
    # ============================================
    # ACTUALIZAR TUTOR
    # ============================================
    def update_tutor(self, tutor_id: int, tutor: Tutor):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            now = datetime.now()
            
            cursor.execute(
                """UPDATE tutors 
                   SET nombre=%s, apellido=%s, cedula=%s, edad=%s, usuario=%s, contraseña=%s, 
                       tipo=%s, especialidad=%s, telefono=%s, email=%s, empresa_id=%s, updated_at=%s 
                   WHERE id=%s""",
                (tutor.nombre, tutor.apellido, tutor.cedula, tutor.edad, tutor.usuario, tutor.contraseña,
                 tutor.tipo, tutor.especialidad, tutor.telefono, tutor.email, tutor.empresa_id, now, tutor_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tutor not found")
            conn.commit()
            return {"result": "Tutor updated successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()

    # ============================================
    # ELIMINAR TUTOR
    # ============================================
    def delete_tutor(self, tutor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tutors WHERE id = %s", (tutor_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tutor not found")
            conn.commit()
            return {"result": "Tutor deleted successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            if conn:
                conn.close()