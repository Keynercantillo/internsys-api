# app/middleware/auth_middleware.py
"""
Middleware de autenticación para proteger rutas
"""

from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
import os

class VerificacionSesionMiddleware(BaseHTTPMiddleware):
    """
    Middleware que verifica la sesión del usuario
    Redirige a login si no hay sesión en rutas protegidas
    """
    
    # Rutas protegidas que requieren autenticación
    RUTAS_EMPRESA = ["/dashboard-empresa"]
    RUTAS_ESTUDIANTE = ["/dashboard-estudiante"]
    RUTAS_PROTEGIDAS = RUTAS_EMPRESA + RUTAS_ESTUDIANTE
    
    async def dispatch(self, request: Request, call_next):
        # Verificar si la ruta está protegida
        ruta_actual = request.url.path
        
        # Obtener el tipo de usuario y sesión de cookies
        tipo_usuario = request.cookies.get("tipo_usuario")
        sesion_token = request.cookies.get("sesion_token")
        
        # Verificar rutas protegidas de empresa
        if ruta_actual in self.RUTAS_EMPRESA:
            if not tipo_usuario == "empresa" or not sesion_token:
                return RedirectResponse(url="/login-empresa", status_code=303)
        
        # Verificar rutas protegidas de estudiante
        elif ruta_actual in self.RUTAS_ESTUDIANTE:
            if not tipo_usuario == "estudiante" or not sesion_token:
                return RedirectResponse(url="/login-estudiante", status_code=303)
        
        # Permitir la solicitud
        response = await call_next(request)
        return response
