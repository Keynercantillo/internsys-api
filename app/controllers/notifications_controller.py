import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.notification_model import Notification
from fastapi.encoders import jsonable_encoder

class NotificationsController:
        
    def create_notification(self, notification: Notification):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notifications (user_email, message, is_read, created_at) VALUES (%s, %s, %s, %s)", (notification.user_email, notification.message, notification.is_read, notification.created_at))
            conn.commit()
            conn.close()
            return {"result": "Notification created"}
        except mysql.connector.Error as err:
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
            cursor.execute("SELECT id, user_email, message, is_read, created_at FROM notifications WHERE id = %s", (notification_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Notification not found")  

            content={
                    'id':int(result[0]),
                    'user_email':result[1],
                    'message':result[2],
                    'is_read':bool(result[3]),
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
       
    def get_notifications(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_email, message, is_read, created_at FROM notifications")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'user_email':data[1],
                    'message':data[2],
                    'is_read':data[3],
                    'created_at':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Notifications not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_notifications_by_user(self, user_email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_email, message, is_read, created_at FROM notifications WHERE user_email = %s ORDER BY created_at DESC", (user_email,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'user_email':data[1],
                    'message':data[2],
                    'is_read':data[3],
                    'created_at':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No notifications found for this user")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_unread_notifications_by_user(self, user_email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_email, message, is_read, created_at FROM notifications WHERE user_email = %s AND is_read = FALSE ORDER BY created_at DESC", (user_email,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'user_email':data[1],
                    'message':data[2],
                    'is_read':data[3],
                    'created_at':data[4]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No unread notifications found for this user")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def mark_as_read(self, notification_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s", (notification_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Notification not found")
            conn.commit()
            return {"result": "Notification marked as read"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def mark_all_as_read(self, user_email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE notifications SET is_read = TRUE WHERE user_email = %s AND is_read = FALSE", (user_email,))
            conn.commit()
            return {"result": f"{cursor.rowcount} notifications marked as read"}
        except mysql.connector.Error as err:
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
                "UPDATE notifications SET user_email=%s, message=%s, is_read=%s, created_at=%s WHERE id=%s",
                (notification.user_email, notification.message, notification.is_read, notification.created_at, notification_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Notification not found")
            conn.commit()
            return {"result": "Notification updated"}
        except mysql.connector.Error as err:
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
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass