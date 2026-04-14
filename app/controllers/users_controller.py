import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.users_model import User
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class UsersController:
    
    # ============================================
    # CREAR USUARIO
    # ============================================
    def create_user(self, user: User):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            empresa_id = getattr(user, 'empresa_id', None)
            
            # Insertar en users
            cursor.execute(
                """INSERT INTO users (nombre, apellido, cedula, edad, usuario, contraseña, rol, email, is_active, last_login, empresa_id) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (user.nombre, user.apellido, user.cedula, user.edad, user.usuario, 
                 user.contraseña, user.rol, user.email, user.is_active, user.last_login, empresa_id)
            )
            new_user_id = cursor.fetchone()[0]
            
            # Si el rol es tutor o docente, insertar también en la tabla tutors
            if user.rol in ['tutor', 'docente']:
                telefono = getattr(user, 'telefono', None)
                tipo = user.rol
                especialidad = getattr(user, 'especialidad', None)
                
                cursor.execute(
                    """INSERT INTO tutors (nombre, apellido, cedula, edad, usuario, contraseña, tipo, telefono, email, empresa_id, especialidad) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user.nombre, user.apellido, user.cedula, user.edad, user.usuario, 
                     user.contraseña, tipo, telefono, user.email, empresa_id, especialidad)
                )
            
            conn.commit()
            conn.close()
            return {"result": "User created successfully", "id": new_user_id, "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # OBTENER USUARIO POR ID
    # ============================================
    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, rol, email, is_active, last_login, empresa_id FROM users WHERE id = %s", 
                (user_id,)
            )
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="User not found")  

            content = {
                'id': int(result[0]),
                'nombre': result[1],
                'apellido': result[2],
                'cedula': result[3],
                'edad': result[4],
                'usuario': result[5],
                'contraseña': result[6],
                'rol': result[7],
                'email': result[8],
                'is_active': result[9],
                'last_login': result[10],
                'empresa_id': result[11]
            }
            return jsonable_encoder(content)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # OBTENER TODOS LOS USUARIOS
    # ============================================
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, rol, email, is_active, last_login, empresa_id FROM users ORDER BY id DESC")
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
                    'rol': data[7],
                    'email': data[8],
                    'is_active': data[9],
                    'last_login': data[10],
                    'empresa_id': data[11]
                }
                payload.append(content)
            if payload:
                return {"result": jsonable_encoder(payload)}
            else:
                return {"result": []}
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # OBTENER USUARIOS POR ROL
    # ============================================
    def get_users_by_role(self, rol: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, rol, email, is_active, last_login, empresa_id FROM users WHERE rol = %s", 
                (rol,)
            )
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
                    'rol': data[7],
                    'email': data[8],
                    'is_active': data[9],
                    'last_login': data[10],
                    'empresa_id': data[11]
                }
                payload.append(content)
            if payload:
                return {"result": jsonable_encoder(payload)}
            else:
                raise HTTPException(status_code=404, detail=f"No users found with role {rol}")  
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # OBTENER USUARIO POR EMAIL
    # ============================================
    def get_user_by_email(self, email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, apellido, cedula, edad, usuario, contraseña, rol, email, is_active, last_login, empresa_id FROM users WHERE email = %s", 
                (email,)
            )
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="User not found")  

            content = {
                'id': int(result[0]),
                'nombre': result[1],
                'apellido': result[2],
                'cedula': result[3],
                'edad': result[4],
                'usuario': result[5],
                'contraseña': result[6],
                'rol': result[7],
                'email': result[8],
                'is_active': result[9],
                'last_login': result[10],
                'empresa_id': result[11]
            }
            return jsonable_encoder(content)
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # ACTUALIZAR USUARIO
    # ============================================
    def update_user(self, user_id: int, user: User):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            empresa_id = getattr(user, 'empresa_id', None)
            
            # Actualizar users
            cursor.execute(
                """UPDATE users 
                   SET nombre=%s, apellido=%s, cedula=%s, edad=%s, usuario=%s, 
                       contraseña=%s, rol=%s, email=%s, is_active=%s, empresa_id=%s 
                   WHERE id=%s""",
                (user.nombre, user.apellido, user.cedula, user.edad, user.usuario, 
                 user.contraseña, user.rol, user.email, user.is_active, empresa_id, user_id),
            )
            
            # Si el rol es tutor o docente, actualizar o insertar en tutors
            if user.rol in ['tutor', 'docente']:
                telefono = getattr(user, 'telefono', None)
                especialidad = getattr(user, 'especialidad', None)
                tipo = user.rol
                
                # Verificar si ya existe en tutors
                cursor.execute("SELECT id FROM tutors WHERE email = %s", (user.email,))
                existing = cursor.fetchone()
                
                if existing:
                    # Actualizar tutor existente
                    cursor.execute(
                        """UPDATE tutors 
                           SET nombre=%s, apellido=%s, cedula=%s, edad=%s, usuario=%s, 
                               contraseña=%s, tipo=%s, telefono=%s, email=%s, empresa_id=%s, especialidad=%s 
                           WHERE email=%s""",
                        (user.nombre, user.apellido, user.cedula, user.edad, user.usuario, 
                         user.contraseña, tipo, telefono, user.email, empresa_id, especialidad, user.email)
                    )
                else:
                    # Insertar nuevo tutor
                    cursor.execute(
                        """INSERT INTO tutors (nombre, apellido, cedula, edad, usuario, contraseña, tipo, telefono, email, empresa_id, especialidad) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (user.nombre, user.apellido, user.cedula, user.edad, user.usuario, 
                         user.contraseña, tipo, telefono, user.email, empresa_id, especialidad)
                    )
            
            if cursor.rowcount == 0 and user.rol not in ['tutor', 'docente']:
                conn.rollback()
                raise HTTPException(status_code=404, detail="User not found")
            
            conn.commit()
            return {"result": "User updated successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass

    # ============================================
    # ELIMINAR USUARIO
    # ============================================
    def delete_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Obtener email y rol del usuario antes de eliminar
            cursor.execute("SELECT email, rol FROM users WHERE id = %s", (user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                email, rol = user_data
                # Si es tutor o docente, eliminar también de tutors
                if rol in ['tutor', 'docente']:
                    cursor.execute("DELETE FROM tutors WHERE email = %s", (email,))
            
            # Eliminar de users
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="User not found")
            
            conn.commit()
            return {"result": "User deleted successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # LOGIN DE USUARIO
    # ============================================
    def login(self, email: str, password: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, nombre, apellido, cedula, edad, usuario, rol, email, empresa_id 
                   FROM users WHERE email = %s AND contraseña = %s AND is_active = true""",
                (email, password)
            )
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=401, detail="Credenciales inválidas o usuario inactivo")
            
            # Actualizar último login
            cursor.execute(
                "UPDATE users SET last_login = NOW() WHERE id = %s",
                (result[0],)
            )
            conn.commit()
            
            content = {
                'id': result[0],
                'nombre': result[1],
                'apellido': result[2],
                'cedula': result[3],
                'edad': result[4],
                'usuario': result[5],
                'rol': result[6],
                'email': result[7],
                'empresa_id': result[8]
            }
            return {"result": content, "message": "Login exitoso", "success": True}
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass