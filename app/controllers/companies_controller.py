import psycopg2
from fastapi import HTTPException
from config.db_config import get_db_connection
from models.company_model import Company
from fastapi.encoders import jsonable_encoder

class CompaniesController:
    
    # ============================================
    # CREAR EMPRESA
    # ============================================
    def create_company(self, company: Company):   
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO companies (name, ruc, address, phone, email, contact_person, sector, status) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id""",
                (company.name, company.ruc, company.address, company.phone, 
                 company.email, company.contact_person, company.sector, company.status)
            )
            new_id = cursor.fetchone()[0]
            conn.commit()
            conn.close()
            return {"result": "Company created successfully", "id": new_id, "success": True}
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
    # OBTENER EMPRESA POR ID
    # ============================================
    def get_company(self, company_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, ruc, address, phone, email, contact_person, sector, status FROM companies WHERE id = %s", 
                (company_id,)
            )
            result = cursor.fetchone()
            if not result:
               raise HTTPException(status_code=404, detail="Company not found")  

            content = {
                'id': int(result[0]),
                'name': result[1],
                'ruc': result[2],
                'address': result[3],
                'phone': result[4],
                'email': result[5],
                'contact_person': result[6],
                'sector': result[7],
                'status': result[8]
            }
            json_data = jsonable_encoder(content)            
            return json_data
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # OBTENER TODAS LAS EMPRESAS
    # ============================================
    def get_companies(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, ruc, address, phone, email, contact_person, sector, status FROM companies ORDER BY id DESC")
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'name': data[1],
                    'ruc': data[2],
                    'address': data[3],
                    'phone': data[4],
                    'email': data[5],
                    'contact_person': data[6],
                    'sector': data[7],
                    'status': data[8]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
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
    # OBTENER EMPRESAS POR SECTOR
    # ============================================
    def get_companies_by_sector(self, sector: str):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, ruc, address, phone, email, contact_person, sector, status FROM companies WHERE sector = %s", 
                (sector,)
            )
            result = cursor.fetchall()
            payload = []
            for data in result:
                content = {
                    'id': data[0],
                    'name': data[1],
                    'ruc': data[2],
                    'address': data[3],
                    'phone': data[4],
                    'email': data[5],
                    'contact_person': data[6],
                    'sector': data[7],
                    'status': data[8]
                }
                payload.append(content)
            json_data = jsonable_encoder(payload)        
            if result:
               return {"result": json_data}
            else:
                raise HTTPException(status_code=404, detail=f"No companies found in sector {sector}")  
        except psycopg2.Error as err:
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass
    
    # ============================================
    # OBTENER EMPRESA POR USUARIO (para login de empresa)
    # ============================================
    def get_company_by_user(self, user_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.name, c.ruc, c.address, c.phone, c.email, c.contact_person, c.sector, c.status 
                FROM companies c
                JOIN users u ON u.empresa_id = c.id
                WHERE u.id = %s
            """, (user_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Company not found for this user")
            content = {
                'id': result[0],
                'name': result[1],
                'ruc': result[2],
                'address': result[3],
                'phone': result[4],
                'email': result[5],
                'contact_person': result[6],
                'sector': result[7],
                'status': result[8]
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
    # ACTUALIZAR EMPRESA
    # ============================================
    def update_company(self, company_id: int, company: Company):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE companies 
                   SET name=%s, ruc=%s, address=%s, phone=%s, email=%s, 
                       contact_person=%s, sector=%s, status=%s 
                   WHERE id=%s""",
                (company.name, company.ruc, company.address, company.phone, 
                 company.email, company.contact_person, company.sector, company.status, company_id),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Company not found")
            conn.commit()
            return {"result": "Company updated successfully", "success": True}
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
    # ELIMINAR EMPRESA
    # ============================================
    def delete_company(self, company_id: int):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM companies WHERE id = %s", (company_id,))
            if cursor.rowcount == 0:
                conn.rollback()
                raise HTTPException(status_code=404, detail="Company not found")
            conn.commit()
            return {"result": "Company deleted successfully", "success": True}
        except psycopg2.Error as err:
            if conn:
                conn.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(err)}")
        finally:
            try:
                conn.close()
            except:
                pass