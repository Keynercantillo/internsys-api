import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.report_model import Report
from fastapi.encoders import jsonable_encoder

class ReportsController:
        
    def create_report(self, report: Report):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO reports (generated_by, report_type, title, content_json, generated_date, file_url, filters_used) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (report.generated_by, report.report_type, report.title, report.content_json,
                 report.generated_date, report.file_url, report.filters_used)
            )
            conn.commit()
            conn.close()
            return {"result": "Report created"}
        except psycopg2.Error as err:
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
            cursor.execute("SELECT id, generated_by, report_type, title, content_json, generated_date, file_url, filters_used FROM reports WHERE id = %s", (report_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Report not found")  

            content = {
                'id': int(result[0]),
                'generated_by': result[1],
                'report_type': result[2],
                'title': result[3],
                'content_json': result[4],
                'generated_date': result[5],
                'file_url': result[6],
                'filters_used': result[7]
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
       
    def get_reports(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, generated_by, report_type, title, content_json, generated_date, file_url, filters_used FROM reports")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'generated_by': data[1],
                    'report_type': data[2],
                    'title': data[3],
                    'content_json': data[4],
                    'generated_date': data[5],
                    'file_url': data[6],
                    'filters_used': data[7]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Reports not found")  
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_reports_by_type(self, report_type: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, generated_by, report_type, title, content_json, generated_date, file_url, filters_used FROM reports WHERE report_type = %s", (report_type,))
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'generated_by': data[1],
                    'report_type': data[2],
                    'title': data[3],
                    'content_json': data[4],
                    'generated_date': data[5],
                    'file_url': data[6],
                    'filters_used': data[7]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No reports found of type {report_type}")  
        except psycopg2.Error as err:
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
                """UPDATE reports SET generated_by=%s, report_type=%s, title=%s, content_json=%s, 
                   generated_date=%s, file_url=%s, filters_used=%s WHERE id=%s""",
                (report.generated_by, report.report_type, report.title, report.content_json,
                 report.generated_date, report.file_url, report.filters_used, report_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Report not found")
            conn.commit()
            return {"result": "Report updated"}
        except psycopg2.Error as err:
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
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass