# ============================================
# CONFIGURACIÓN DE CORREO ELECTRÓNICO
# ============================================

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Gmail (o cualquier SMTP)
EMAIL_CONFIG = {
    "SMTP_SERVER": "smtp.gmail.com",
    "SMTP_PORT": 587,
    "SENDER_EMAIL": os.getenv("EMAIL_USER", "tu_correo@gmail.com"),
    "SENDER_PASSWORD": os.getenv("EMAIL_PASSWORD", "tu_contraseña_de_aplicacion"),
    "ADMIN_EMAIL": os.getenv("ADMIN_EMAIL", "admin@internsys.com")
}

# Para usar Gmail, necesitas:
# 1. Activar verificación en dos pasos
# 2. Generar contraseña de aplicación en: https://myaccount.google.com/apppasswords