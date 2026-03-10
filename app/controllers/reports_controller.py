import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.report_model import Report
from fastapi.encoders import jsonable_encoder

class ReportsController:
        
    def create_report(self, report: Report):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reports (student_name, file_url, submission_date) VALUES (%s, %s, %s)", (report.student_name, report.file_url, report.submission_date))
            conn.commit()
            conn.close()
            return {"result": "Report created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_report(self, report_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, file_url, submission_date FROM reports WHERE id = %s", (report_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Report not found")  

            content={
                    'id':int(result[0]),
                    'student_name':result[1],
                    'file_url':result[2],
                    'submission_date':result[3]
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
       
    def get_reports(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, file_url, submission_date FROM reports")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'file_url':data[2],
                    'submission_date':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Reports not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_reports_by_student(self, student_name: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, student_name, file_url, submission_date FROM reports WHERE student_name = %s ORDER BY submission_date DESC", (student_name,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'student_name':data[1],
                    'file_url':data[2],
                    'submission_date':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="No reports found for this student")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def update_report(self, report_id: int, report: Report):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE reports SET student_name=%s, file_url=%s, submission_date=%s WHERE id=%s",
                (report.student_name, report.file_url, report.submission_date, report_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Report not found")
            conn.commit()
            return {"result": "Report updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_report(self, report_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reports WHERE id = %s", (report_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Report not found")
            conn.commit()
            return {"result": "Report deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass