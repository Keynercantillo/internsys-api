import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.notification_model import Notification
from fastapi.encoders import jsonable_encoder
from datetime import datetime

class NotificationsController:
        
    def create_notification(self, notification: Notification):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            if notification.created_at is None:
                notification.created_at = datetime.now()
            cursor.execute(
                """INSERT INTO notifications (user_id, title, message, type, read, created_at, link_url) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (notification.user_id, notification.title, notification.message, notification.type,
                 notification.read, notification.created_at, notification.link_url)
            )
            conn.commit()
            conn.close()
            return {"result": "Notification created"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        
    def get_notification(self, notification_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, title, message, type, read, created_at, link_url FROM notifications WHERE id = %s", (notification_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Notification not found")  

            content = {
                'id': int(result[0]),
                'user_id': result[1],
                'title': result[2],
                'message': result[3],
                'type': result[4],
                'read': result[5],
                'created_at': result[6],
                'link_url': result[7]
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
       
    def get_notifications(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, title, message, type, read, created_at, link_url FROM notifications")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'user_id': data[1],
                    'title': data[2],
                    'message': data[3],
                    'type': data[4],
                    'read': data[5],
                    'created_at': data[6],
                    'link_url': data[7]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Notifications not found")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_notifications_by_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, title, message, type, read, created_at, link_url FROM notifications WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'user_id': data[1],
                    'title': data[2],
                    'message': data[3],
                    'type': data[4],
                    'read': data[5],
                    'created_at': data[6],
                    'link_url': data[7]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No notifications found for user {user_id}")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_notification(self, notification_id: int, notification: Notification):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE notifications SET user_id=%s, title=%s, message=%s, type=%s, read=%s, created_at=%s, link_url=%s WHERE id=%s""",
                (notification.user_id, notification.title, notification.message, notification.type,
                 notification.read, notification.created_at, notification.link_url, notification_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Notification not found")
            conn.commit()
            return {"result": "Notification updated"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_notification(self, notification_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Notification not found")
            conn.commit()
            return {"result": "Notification deleted"}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass