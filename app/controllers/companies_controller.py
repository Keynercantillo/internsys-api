import mysql
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.company_model import Company
from fastapi.encoders import jsonable_encoder

class CompaniesController:
        
    def create_company(self, company: Company):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO companies (company_name, user_email, tax_id_number) VALUES (%s, %s, %s)", (company.company_name, company.user_email, company.tax_id_number))
            conn.commit()
            conn.close()
            return {"result": "Company created"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
        

    def get_company(self, company_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, user_email, tax_id_number FROM companies WHERE id = %s", (company_id,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Company not found")  

            content={
                    'id':int(result[0]),
                    'company_name':result[1],
                    'user_email':result[2],
                    'tax_id_number':result[3]
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
       
    def get_companies(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, user_email, tax_id_number FROM companies")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content={
                    'id':data[0],
                    'company_name':data[1],
                    'user_email':data[2],
                    'tax_id_number':data[3]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail="Companies not found")  
                
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass
    
    def get_company_by_email(self, user_email: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, user_email, tax_id_number FROM companies WHERE user_email = %s", (user_email,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Company not found")  

            content={
                    'id':int(result[0]),
                    'company_name':result[1],
                    'user_email':result[2],
                    'tax_id_number':result[3]
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
    
    def get_company_by_tax_id(self, tax_id_number: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, company_name, user_email, tax_id_number FROM companies WHERE tax_id_number = %s", (tax_id_number,))
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Company not found")  

            content={
                    'id':int(result[0]),
                    'company_name':result[1],
                    'user_email':result[2],
                    'tax_id_number':result[3]
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
    
    def update_company(self, company_id: int, company: Company):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE companies SET company_name=%s, user_email=%s, tax_id_number=%s WHERE id=%s",
                (company.company_name, company.user_email, company.tax_id_number, company_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Company not found")
            conn.commit()
            return {"result": "Company updated"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass

    def delete_company(self, company_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM companies WHERE id = %s", (company_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Company not found")
            conn.commit()
            return {"result": "Company deleted"}
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=str(err))
        finally:
            try:
                conn.close()
            except:
                pass