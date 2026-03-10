import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.users_model import User
from fastapi.encoders import jsonable_encoder

class UsersController:
        
    def create_user(self, user: User):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password_hash, role, created_at) VALUES (%s, %s, %s, %s)", (user.email, user.password_hash, user.role, user.created_at))
            conn.commit()
            conn.close()
            return {"result": "User created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, role, created_at FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="User not found")  

            content={
                    'id':int(result[0]),
                    'email':result[1],
                    'password_hash':result[2],
                    'role':result[3],
                    'created_at':result[4]
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
       
    def get_users(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, role, created_at FROM users")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'email':data[1],
                    'password_hash':data[2],
                    'role':data[3],
                    'created_at':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Users not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_users_by_role(self, role: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, role, created_at FROM users WHERE role = %s", (role,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'email':data[1],
                    'password_hash':data[2],
                    'role':data[3],
                    'created_at':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No users found with role {role}")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_user_by_email(self, email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, password_hash, role, created_at FROM users WHERE email = %s", (email,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="User not found")  

            content={
                    'id':int(result[0]),
                    'email':result[1],
                    'password_hash':result[2],
                    'role':result[3],
                    'created_at':result[4]
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
    
    def update_user(self, user_id: int, user: User):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET email=%s, password_hash=%s, role=%s, created_at=%s WHERE id=%s",
                (user.email, user.password_hash, user.role, user.created_at, user_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="User not found")
            conn.commit()
            return {"result": "User updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="User not found")
            conn.commit()
            return {"result": "User deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass