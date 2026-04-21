from fastapi import APIRouter
from pydantic import BaseModel
from utils.email_service import EmailService

router = APIRouter()

class ReporteNotification(BaseModel):
    usuario: dict
    filtros: str
    total_registros: int

@router.post("/notificar_reporte")
async def notificar_reporte(data: ReporteNotification):
    """Notifica por correo cuando se genera un reporte"""
    EmailService.notificar_reporte_generado(
        data.usuario, 
        data.filtros, 
        data.total_registros, 
        "admin@internsys.com"
    )
    return {"message": "Notificación enviada", "success": True}