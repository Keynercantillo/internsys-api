# ============================================
# SERVICIO DE NOTIFICACIONES POR CORREO
# ============================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config.email_config import EMAIL_CONFIG

class EmailService:
    
    @staticmethod
    def enviar_correo(destinatario, asunto, cuerpo_html):
        """Envía un correo electrónico"""
        try:
            if not destinatario or destinatario == 'None':
                print(f"⚠️ Destinatario no válido: {destinatario}")
                return False
            
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG["SENDER_EMAIL"]
            msg['To'] = destinatario
            msg['Subject'] = asunto
            
            msg.attach(MIMEText(cuerpo_html, 'html'))
            
            server = smtplib.SMTP(EMAIL_CONFIG["SMTP_SERVER"], EMAIL_CONFIG["SMTP_PORT"])
            server.starttls()
            server.login(EMAIL_CONFIG["SENDER_EMAIL"], EMAIL_CONFIG["SENDER_PASSWORD"])
            server.send_message(msg)
            server.quit()
            print(f"✅ Correo enviado a {destinatario}")
            return True
        except Exception as e:
            print(f"❌ Error enviando correo: {e}")
            return False
    
    # ============================================
    # NOTIFICACIONES ESPECÍFICAS
    # ============================================
    
    @staticmethod
    def notificar_eliminacion_usuario(usuario_eliminado, admin_email):
        """Notifica cuando se elimina un usuario"""
        asunto = "⚠️ Usuario Eliminado - InternSys"
        cuerpo = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; background: #f4f6f9; }}
                .header {{ background: #ef476f; color: white; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 20px; border-radius: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                td {{ padding: 10px; }}
                .bg-gray {{ background: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>⚠️ Usuario Eliminado</h2>
                </div>
                <div class="content">
                    <p>Se ha eliminado un usuario del sistema.</p>
                    <table>
                        <tr><td class="bg-gray"><strong>ID:</strong></td><td>{usuario_eliminado.get('id', 'N/A')}</td></tr>
                        <tr><td><strong>Nombre:</strong></td><td>{usuario_eliminado.get('nombre', 'N/A')} {usuario_eliminado.get('apellido', '')}</td></tr>
                        <tr><td class="bg-gray"><strong>Email:</strong></td><td>{usuario_eliminado.get('email', 'N/A')}</td></tr>
                        <tr><td><strong>Rol:</strong></td><td>{usuario_eliminado.get('rol', 'N/A')}</td></tr>
                        <tr><td class="bg-gray"><strong>Fecha eliminación:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                    </table>
                    <p style="margin-top: 20px;">Este es un mensaje automático del sistema InternSys.</p>
                </div>
                <div class="footer">
                    <p>InternSys - Sistema de Gestión de Pasantías</p>
                </div>
            </div>
        </body>
        </html>
        """
        return EmailService.enviar_correo(admin_email, asunto, cuerpo)
    
    @staticmethod
    def notificar_nuevo_usuario(usuario, admin_email):
        """Notifica cuando se crea un nuevo usuario"""
        asunto = "👤 Nuevo Usuario Registrado - InternSys"
        cuerpo = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; background: #f4f6f9; }}
                .header {{ background: #118ab2; color: white; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 20px; border-radius: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                td {{ padding: 10px; }}
                .bg-gray {{ background: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>👤 Nuevo Usuario Registrado</h2>
                </div>
                <div class="content">
                    <p>Se ha registrado un nuevo usuario en el sistema.</p>
                    <table>
                        <tr><td class="bg-gray"><strong>Nombre:</strong></td><td>{usuario.get('nombre', 'N/A')} {usuario.get('apellido', '')}</td></tr>
                        <tr><td><strong>Email:</strong></td><td>{usuario.get('email', 'N/A')}</td></tr>
                        <tr><td class="bg-gray"><strong>Rol:</strong></td><td>{usuario.get('rol', 'N/A')}</td></tr>
                        <tr><td><strong>Fecha registro:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                    </table>
                </div>
                <div class="footer">
                    <p>InternSys - Sistema de Gestión de Pasantías</p>
                </div>
            </div>
        </body>
        </html>
        """
        return EmailService.enviar_correo(admin_email, asunto, cuerpo)
    
    @staticmethod
    def notificar_asignacion_estudiante(estudiante, oferta, tutor, empresa):
        """Notifica cuando se asigna un estudiante a un tutor"""
        asunto = "🎓 Nueva Asignación de Pasantía - InternSys"
        
        # Correo para el tutor
        cuerpo_tutor = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; background: #f4f6f9; }}
                .header {{ background: #06d6a0; color: white; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 20px; border-radius: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h2>🎓 Nueva Asignación</h2></div>
                <div class="content">
                    <p>Se te ha asignado un nuevo estudiante para la pasantía.</p>
                    <p><strong>Estudiante:</strong> {estudiante.get('nombre', 'N/A')} {estudiante.get('apellido', '')}</p>
                    <p><strong>Oferta:</strong> {oferta.get('title', 'N/A')}</p>
                    <p><strong>Empresa:</strong> {empresa.get('name', 'N/A')}</p>
                    <p><strong>Fecha inicio:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
                    <p>Ingresa al sistema para ver más detalles.</p>
                </div>
                <div class="footer"><p>InternSys - Sistema de Gestión de Pasantías</p></div>
            </div>
        </body>
        </html>
        """
        
        # Correo para el estudiante
        cuerpo_estudiante = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; background: #f4f6f9; }}
                .header {{ background: #06d6a0; color: white; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 20px; border-radius: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h2>🎓 Has sido asignado a una pasantía</h2></div>
                <div class="content">
                    <p>¡Felicidades! Has sido asignado a una pasantía.</p>
                    <p><strong>Oferta:</strong> {oferta.get('title', 'N/A')}</p>
                    <p><strong>Empresa:</strong> {empresa.get('name', 'N/A')}</p>
                    <p><strong>Tutor:</strong> {tutor.get('nombre', 'N/A')} {tutor.get('apellido', '')}</p>
                    <p>Ingresa al sistema para ver más detalles y comenzar tu pasantía.</p>
                </div>
                <div class="footer"><p>InternSys - Sistema de Gestión de Pasantías</p></div>
            </div>
        </body>
        </html>
        """
        
        EmailService.enviar_correo(tutor.get('email'), asunto, cuerpo_tutor)
        EmailService.enviar_correo(estudiante.get('email'), asunto, cuerpo_estudiante)
        return True
    
    @staticmethod
    def notificar_postulacion_estudiante(estudiante, oferta, empresa):
        """Notifica cuando un estudiante postula a una oferta"""
        asunto = "📝 Nueva Postulación - InternSys"
        
        cuerpo_empresa = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; background: #f4f6f9; }}
                .header {{ background: #ffd166; color: #333; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 20px; border-radius: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h2>📝 Nueva Postulación Recibida</h2></div>
                <div class="content">
                    <p>Un estudiante ha postulado a una de tus ofertas.</p>
                    <p><strong>Estudiante:</strong> {estudiante.get('nombre', 'N/A')} {estudiante.get('apellido', '')}</p>
                    <p><strong>Carrera:</strong> {estudiante.get('carrera', 'N/A')}</p>
                    <p><strong>Oferta:</strong> {oferta.get('title', 'N/A')}</p>
                    <p>Ingresa al sistema para revisar la postulación.</p>
                </div>
                <div class="footer"><p>InternSys - Sistema de Gestión de Pasantías</p></div>
            </div>
        </body>
        </html>
        """
        
        cuerpo_estudiante = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; background: #f4f6f9; }}
                .header {{ background: #ffd166; color: #333; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 20px; border-radius: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h2>✅ Postulación Enviada</h2></div>
                <div class="content">
                    <p>Tu postulación ha sido enviada correctamente.</p>
                    <p><strong>Oferta:</strong> {oferta.get('title', 'N/A')}</p>
                    <p><strong>Empresa:</strong> {empresa.get('name', 'N/A')}</p>
                    <p>La empresa revisará tu solicitud y te contactará pronto.</p>
                </div>
                <div class="footer"><p>InternSys - Sistema de Gestión de Pasantías</p></div>
            </div>
        </body>
        </html>
        """
        
        EmailService.enviar_correo(empresa.get('email'), asunto, cuerpo_empresa)
        EmailService.enviar_correo(estudiante.get('email'), asunto, cuerpo_estudiante)
        return True
    
    @staticmethod
    def notificar_reporte_generado(usuario, filtros, total_registros, admin_email):
        """Notifica cuando se genera un reporte"""
        asunto = "📊 Reporte Generado - InternSys"
        cuerpo = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .container {{ padding: 20px; background: #f4f6f9; }}
                .header {{ background: #118ab2; color: white; padding: 15px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: white; padding: 20px; border-radius: 10px; }}
                .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                td {{ padding: 10px; }}
                .bg-gray {{ background: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header"><h2>📊 Reporte Generado</h2></div>
                <div class="content">
                    <p>Se ha generado un nuevo reporte en el sistema.</p>
                    <table>
                        <tr><td class="bg-gray"><strong>Generado por:</strong></td><td>{usuario.get('nombre', 'Admin')} {usuario.get('apellido', '')}</td></tr>
                        <tr><td><strong>Fecha:</strong></td><td>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td></tr>
                        <tr><td class="bg-gray"><strong>Filtros aplicados:</strong></td><td>{filtros}</td></tr>
                        <tr><td><strong>Total registros:</strong></td><td>{total_registros}</td></tr>
                    </table>
                </div>
                <div class="footer"><p>InternSys - Sistema de Gestión de Pasantías</p></div>
            </div>
        </body>
        </html>
        """
        return EmailService.enviar_correo(admin_email, asunto, cuerpo)