import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.profile_model import Profile
from fastapi.encoders import jsonable_encoder

class ProfilesController:
        
    def create_profile(self, profile: Profile):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO profiles (user_id, bio, phone, address, birth_date, profile_picture_url, social_links) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (profile.user_id, profile.bio, profile.phone, profile.address, profile.birth_date,
                 profile.profile_picture_url, profile.social_links)
            )
            conn.commit()
            conn.close()
            return {"result": "Profile created"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        
    def get_profile(self, profile_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, bio, phone, address, birth_date, profile_picture_url, social_links FROM profiles WHERE id = %s", (profile_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Profile not found")  

            content = {
                'id': int(result[0]),
                'user_id': result[1],
                'bio': result[2],
                'phone': result[3],
                'address': result[4],
                'birth_date': result[5],
                'profile_picture_url': result[6],
                'social_links': result[7]
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
       
    def get_profiles(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, bio, phone, address, birth_date, profile_picture_url, social_links FROM profiles")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'user_id': data[1],
                    'bio': data[2],
                    'phone': data[3],
                    'address': data[4],
                    'birth_date': data[5],
                    'profile_picture_url': data[6],
                    'social_links': data[7]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Profiles not found")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_profile_by_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, bio, phone, address, birth_date, profile_picture_url, social_links FROM profiles WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Profile not found for this user")  

            content = {
                'id': int(result[0]),
                'user_id': result[1],
                'bio': result[2],
                'phone': result[3],
                'address': result[4],
                'birth_date': result[5],
                'profile_picture_url': result[6],
                'social_links': result[7]
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
    
    def update_profile(self, profile_id: int, profile: Profile):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE profiles SET user_id=%s, bio=%s, phone=%s, address=%s, birth_date=%s, 
                   profile_picture_url=%s, social_links=%s WHERE id=%s""",
                (profile.user_id, profile.bio, profile.phone, profile.address, profile.birth_date,
                 profile.profile_picture_url, profile.social_links, profile_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Profile not found")
            conn.commit()
            return {"result": "Profile updated"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_profile(self, profile_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM profiles WHERE id = %s", (profile_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Profile not found")
            conn.commit()
            return {"result": "Profile deleted"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass