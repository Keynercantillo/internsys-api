from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2 import Error

router = APIRouter()

# ============================================
# CONEXIÓN A POSTGRESQL (NEON.TECH)
# ============================================
def get_db_connection():
    return psycopg2.connect(
        host="ep-weathered-credit-amp6j2mh-pooler.c-5.us-east-1.aws.neon.tech",
        port="5432",
        user="neondb_owner",
        password="npg_dY7fIsqmQU9n",
        dbname="neondb",
        sslmode="require"
    )

# ============================================
# MODELOS PYDANTIC
# ============================================

class AceptarPostulacionRequest(BaseModel):
    postulacion_id: int
    administrador_id: int

class DenegarPostulacionRequest(BaseModel):
    postulacion_id: int
    administrador_id: int
    motivo: Optional[str] = None

# ============================================
# NOTIFICACIONES DE POSTULACIONES
# ============================================

@router.post("/aceptar_postulacion")
async def aceptar_postulacion(data: AceptarPostulacionRequest):
    """Acepta una postulación y envía notificación al estudiante"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # 1. Verificar que la postulación existe
        cursor.execute(
            "SELECT id, student_id, offer_id FROM applications WHERE id = %s",
            (data.postulacion_id,)
        )
        postulacion = cursor.fetchone()
        
        if not postulacion:
            raise HTTPException(status_code=404, detail="Postulación no encontrada")
        
        # 2. Actualizar estado de la postulación a 'Aceptada'
        cursor.execute(
            "UPDATE applications SET estado = 'Aceptada', updated_at = NOW() WHERE id = %s",
            (data.postulacion_id,)
        )
        
        # 3. Obtener nombre de la oferta para el mensaje
        cursor.execute(
            "SELECT title FROM internship_offers WHERE id = %s",
            (postulacion[2],)  # offer_id está en índice 2
        )
        oferta = cursor.fetchone()
        nombre_oferta = oferta[0] if oferta else "la oferta"
        
        # 4. Crear notificación en application_notifications
        mensaje = f"✅ ¡Felicidades! Tu postulación para '{nombre_oferta}' ha sido ACEPTADA."
        cursor.execute(
            """INSERT INTO application_notifications 
               (application_id, user_id, message, is_read, created_at) 
               VALUES (%s, %s, %s, false, NOW())""",
            (data.postulacion_id, postulacion[1], mensaje)  # student_id está en índice 1
        )
        
        connection.commit()
        
        return {
            "message": "Postulación aceptada y notificación enviada",
            "success": True,
            "notification_id": cursor.lastrowid,
            "estudiante_id": postulacion[1]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.post("/denegar_postulacion")
async def denegar_postulacion(data: DenegarPostulacionRequest):
    """Deniega una postulación y envía notificación al estudiante"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # 1. Verificar que la postulación existe
        cursor.execute(
            "SELECT id, student_id, offer_id FROM applications WHERE id = %s",
            (data.postulacion_id,)
        )
        postulacion = cursor.fetchone()
        
        if not postulacion:
            raise HTTPException(status_code=404, detail="Postulación no encontrada")
        
        # 2. Actualizar estado de la postulación a 'Rechazada'
        cursor.execute(
            "UPDATE applications SET estado = 'Rechazada', updated_at = NOW() WHERE id = %s",
            (data.postulacion_id,)
        )
        
        # 3. Obtener nombre de la oferta para el mensaje
        cursor.execute(
            "SELECT title FROM internship_offers WHERE id = %s",
            (postulacion[2],)
        )
        oferta = cursor.fetchone()
        nombre_oferta = oferta[0] if oferta else "la oferta"
        
        # 4. Crear mensaje con motivo si existe
        mensaje = f"❌ Lo sentimos. Tu postulación para '{nombre_oferta}' ha sido DENEGADA."
        if data.motivo:
            mensaje += f" Motivo: {data.motivo}"
        
        # 5. Crear notificación
        cursor.execute(
            """INSERT INTO application_notifications 
               (application_id, user_id, message, is_read, created_at) 
               VALUES (%s, %s, %s, false, NOW())""",
            (data.postulacion_id, postulacion[1], mensaje)
        )
        
        connection.commit()
        
        return {
            "message": "Postulación denegada y notificación enviada",
            "success": True,
            "notification_id": cursor.lastrowid,
            "estudiante_id": postulacion[1]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


# ============================================
# OBTENER NOTIFICACIONES
# ============================================

@router.get("/mis_notificaciones/{estudiante_id}")
async def obtener_notificaciones(estudiante_id: int):
    """Obtiene todas las notificaciones de un estudiante"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            """SELECT id, application_id, user_id, message, is_read, 
                      TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') as created_at
               FROM application_notifications 
               WHERE user_id = %s 
               ORDER BY created_at DESC""",
            (estudiante_id,)
        )
        rows = cursor.fetchall()
        
        notificaciones = []
        for row in rows:
            notificaciones.append({
                "id": row[0],
                "application_id": row[1],
                "user_id": row[2],
                "message": row[3],
                "is_read": row[4],
                "created_at": row[5]
            })
        
        return {
            "success": True,
            "total": len(notificaciones),
            "notificaciones": notificaciones
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.get("/notificaciones_no_leidas/{estudiante_id}")
async def contar_notificaciones_no_leidas(estudiante_id: int):
    """Cuenta las notificaciones no leídas de un estudiante"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            """SELECT COUNT(*) as total 
               FROM application_notifications 
               WHERE user_id = %s AND is_read = false""",
            (estudiante_id,)
        )
        result = cursor.fetchone()
        total = result[0] if result else 0
        
        return {
            "success": True,
            "estudiante_id": estudiante_id,
            "no_leidas": total
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.put("/marcar_notificacion_leida/{notificacion_id}")
async def marcar_notificacion_como_leida(notificacion_id: int):
    """Marca una notificación específica como leída"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            "UPDATE application_notifications SET is_read = true WHERE id = %s",
            (notificacion_id,)
        )
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Notificación no encontrada")
        
        connection.commit()
        
        return {
            "success": True,
            "message": "Notificación marcada como leída"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()


@router.put("/marcar_todas_notificaciones_leidas/{estudiante_id}")
async def marcar_todas_notificaciones_como_leidas(estudiante_id: int):
    """Marca todas las notificaciones de un estudiante como leídas"""
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute(
            """UPDATE application_notifications 
               SET is_read = true 
               WHERE user_id = %s AND is_read = false""",
            (estudiante_id,)
        )
        
        connection.commit()
        
        return {
            "success": True,
            "message": f"{cursor.rowcount} notificaciones marcadas como leídas",
            "actualizadas": cursor.rowcount
        }
        
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        connection.close()