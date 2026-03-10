from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import sys
import os

# Agregar el directorio actual al path para evitar errores de importación
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar todas las rutas
from routes.students_routes import router as students_router
from routes.companies_routes import router as companies_router
from routes.tutors_routes import router as tutors_router
from routes.internship_offers_routes import router as internship_offers_router
from routes.internship_assignments_routes import router as internship_assignments_router
from routes.users_routes import router as users_router
from routes.agreements_routes import router as agreements_router
from routes.followup_visits_routes import router as followup_visits_router
from routes.reports_routes import router as reports_router
from routes.evaluations_routes import router as evaluations_router
from routes.notifications_routes import router as notifications_router

app = FastAPI(
    title="Internship Management API",
    description="API para gestión de prácticas profesionales",
    version="1.0.0"
)

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar templates y archivos estáticos
try:
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    print("⚠️  Carpeta 'templates' o 'static' no encontrada. El HTML no estará disponible.")

# Incluir todas las rutas de la API
app.include_router(students_router, prefix="/api", tags=["Students"])
app.include_router(companies_router, prefix="/api", tags=["Companies"])
app.include_router(tutors_router, prefix="/api", tags=["Tutors"])
app.include_router(internship_offers_router, prefix="/api", tags=["Internship Offers"])
app.include_router(internship_assignments_router, prefix="/api", tags=["Internship Assignments"])
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(agreements_router, prefix="/api", tags=["Agreements"])
app.include_router(followup_visits_router, prefix="/api", tags=["Follow-up Visits"])
app.include_router(reports_router, prefix="/api", tags=["Reports"])
app.include_router(evaluations_router, prefix="/api", tags=["Evaluations"])
app.include_router(notifications_router, prefix="/api", tags=["Notifications"])

# Ruta principal para servir el HTML
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except:
        return """
        <html>
            <head><title>API funcionando</title></head>
            <body>
                <h1>🚀 API funcionando correctamente</h1>
                <p>El HTML no está configurado. Usa <a href="/docs">/docs</a> para ver la documentación.</p>
            </body>
        </html>
        """

# Ruta de health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "message": "API funcionando correctamente",
        "version": "1.0.0"
    }

# Ruta para ver todas las rutas disponibles
@app.get("/routes")
async def list_routes():
    routes = []
    for route in app.routes:
        routes.append({
            "path": route.path,
            "name": route.name,
            "methods": list(route.methods) if hasattr(route, "methods") else []
        })
    return {"routes": routes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )