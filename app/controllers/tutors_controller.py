import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.tutor_model import Tutor
from fastapi.encoders import jsonable_encoder

class TutorsController:
        
    def create_tutor(self, tutor: Tutor):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO tutors (nombre, apellido, cedula, edad, usuario, contraseña, tipo, especialidad, telefono, email, empresa_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (tutor.nombre, tutor.apellido, tutor.cedula, tutor.edad, tutor.usuario, tutor.contraseña,
                 tutor.tipo, tutor.especialidad, tutor.telefono, tutor.email, tutor.empresa_id)
            )
            conn.commit()
            conn.close()
            return {"result": "Tutor created"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        
    def get_tutor(self, tutor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, tipo, especialidad, telefono, email, empresa_id FROM tutors WHERE id = %s", (tutor_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Tutor not found")  

            content = {
                'id': int(result[0]), 'nombre': result[1], 'apellido': result[2], 'cedula': result[3],
                'edad': result[4], 'usuario': result[5], 'contraseña': result[6], 'tipo': result[7],
                'especialidad': result[8], 'telefono': result[9], 'email': result[10], 'empresa_id': result[11]
            }
            return jsonable_encoder(content)
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
       
    def get_tutors(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, tipo, especialidad, telefono, email, empresa_id FROM tutors")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'nombre': data[1], 'apellido': data[2], 'cedula': data[3],
                    'edad': data[4], 'usuario': data[5], 'contraseña': data[6], 'tipo': data[7],
                    'especialidad': data[8], 'telefono': data[9], 'email': data[10], 'empresa_id': data[11]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Tutors not found")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_tutors_by_type(self, tipo: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, tipo, especialidad, telefono, email, empresa_id FROM tutors WHERE tipo = %s", (tipo,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0], 'nombre': data[1], 'apellido': data[2], 'cedula': data[3],
                    'edad': data[4], 'usuario': data[5], 'contraseña': data[6], 'tipo': data[7],
                    'especialidad': data[8], 'telefono': data[9], 'email': data[10], 'empresa_id': data[11]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No tutors found of type {tipo}")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_tutor(self, tutor_id: int, tutor: Tutor):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE tutors SET nombre=%s, apellido=%s, cedula=%s, edad=%s, usuario=%s, contraseña=%s, 
                   tipo=%s, especialidad=%s, telefono=%s, email=%s, empresa_id=%s WHERE id=%s""",
                (tutor.nombre, tutor.apellido, tutor.cedula, tutor.edad, tutor.usuario, tutor.contraseña,
                 tutor.tipo, tutor.especialidad, tutor.telefono, tutor.email, tutor.empresa_id, tutor_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tutor not found")
            conn.commit()
            return {"result": "Tutor updated"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_tutor(self, tutor_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tutors WHERE id = %s", (tutor_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Tutor not found")
            conn.commit()
            return {"result": "Tutor deleted"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass