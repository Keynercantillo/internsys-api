from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ============================================
# IMPORTAR TODOS LOS ROUTERS
# ============================================
from routes.users_routes import router as users_router
from routes.students_routes import router as students_router
from routes.companies_routes import router as companies_router
from routes.tutors_routes import router as tutors_router
from routes.internship_offers_routes import router as internship_offers_router
from routes.internship_assignments_routes import router as internship_assignments_router
from routes.agreements_routes import router as agreements_router
from routes.evaluations_routes import router as evaluations_router
from routes.followup_visits_routes import router as followup_visits_router
from routes.notifications_routes import router as notifications_router
from routes.profiles_routes import router as profiles_router
from routes.reports_routes import router as reports_router
from routes.auth_routes import router as auth_router
from routes.applications_routes import router as applications_router  # ✅ NUEVO

# ============================================
# CREAR APLICACIÓN FASTAPI
# ============================================
app = FastAPI(
    title="InternSys API",
    description="API para gestión de prácticas profesionales",
    version="2.0.0"
)

# ============================================
# CONFIGURACIÓN CORS
# ============================================
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://localhost:5500",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# SERVIR FRONTEND ESTÁTICO
# ============================================

# Obtener la ruta absoluta al directorio frontend
FRONTEND_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend")

# Verificar si existe la carpeta frontend
if os.path.exists(FRONTEND_DIR):
    # Montar archivos estáticos (CSS, JS, COMPONENTS, assets)
    css_dir = os.path.join(FRONTEND_DIR, "css")
    js_dir = os.path.join(FRONTEND_DIR, "js")
    components_dir = os.path.join(FRONTEND_DIR, "components")
    assets_dir = os.path.join(FRONTEND_DIR, "assets")
    
    if os.path.exists(css_dir):
        app.mount("/css", StaticFiles(directory=css_dir), name="css")
        print(f"✅ CSS montado en: {css_dir}")
    
    if os.path.exists(js_dir):
        app.mount("/js", StaticFiles(directory=js_dir), name="js")
        print(f"✅ JS montado en: {js_dir}")
    
    if os.path.exists(components_dir):
        app.mount("/components", StaticFiles(directory=components_dir), name="components")
        print(f"✅ Components montado en: {components_dir}")
    
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
        print(f"✅ Assets montado en: {assets_dir}")
    
    print(f"✅ Frontend encontrado en: {FRONTEND_DIR}")
else:
    print(f"⚠️ No se encontró la carpeta frontend en: {FRONTEND_DIR}")

# Ruta para servir el index.html
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("""
    <html>
        <head><title>InternSys</title></head>
        <body>
            <h1>InternSys API</h1>
            <p>Frontend no encontrado. Asegúrate de tener la carpeta 'frontend' en el mismo nivel que 'app'.</p>
            <p>Documentación API: <a href="/docs">/docs</a></p>
        </body>
    </html>
    """)

# Ruta para servir cualquier archivo HTML del frontend
@app.get("/{html_file}")
async def serve_html(html_file: str):
    # Seguridad: solo permitir archivos .html
    if not html_file.endswith('.html'):
        return {"error": "Solo se permiten archivos HTML"}
    
    file_path = os.path.join(FRONTEND_DIR, html_file)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return HTMLResponse(f"<h1>404</h1><p>Archivo {html_file} no encontrado</p>", status_code=404)

# ============================================
# INCLUIR TODAS LAS RUTAS DE LA API
# ============================================

# Rutas de autenticación
app.include_router(auth_router)

# Rutas de recursos (con prefijo /api)
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(students_router, prefix="/api", tags=["Students"])
app.include_router(companies_router, prefix="/api", tags=["Companies"])
app.include_router(tutors_router, prefix="/api", tags=["Tutors"])
app.include_router(internship_offers_router, prefix="/api", tags=["Internship Offers"])
app.include_router(internship_assignments_router, prefix="/api", tags=["Internship Assignments"])
app.include_router(agreements_router, prefix="/api", tags=["Agreements"])
app.include_router(evaluations_router, prefix="/api", tags=["Evaluations"])
app.include_router(followup_visits_router, prefix="/api", tags=["Follow-up Visits"])
app.include_router(notifications_router, prefix="/api", tags=["Notifications"])
app.include_router(profiles_router, prefix="/api", tags=["Profiles"])
app.include_router(reports_router, prefix="/api", tags=["Reports"])
app.include_router(applications_router, prefix="/api", tags=["Applications"])  # ✅ NUEVO

# ============================================
# RUTAS ADICIONALES DE LA API
# ============================================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "version": "2.0.0"
    }

@app.get("/routes")
async def list_routes():
    routes_list = []
    for route in app.routes:
        if hasattr(route, "methods") and route.methods:
            routes_list.append({
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods)
            })
    return {
        "total_routes": len(routes_list),
        "routes": routes_list
    }

# ============================================
# EJECUCIÓN DEL SERVIDOR
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("🚀 InternSys API - Servidor Iniciado")
    print("="*60)
    print(f"📚 Documentación API: http://localhost:8000/docs")
    print(f"🌐 Frontend: http://localhost:8000")
    print(f"❤️ Health: http://localhost:8000/health")
    print("="*60)
    print("✨ Servidor corriendo con recarga automática")
    print("="*60)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )