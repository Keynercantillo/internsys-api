from fastapi import APIRouter, HTTPException
from controllers.offers_controller import OffersController
from models.offer_model import InternshipOffer

router = APIRouter()
offers_controller = OffersController()

# ============================================
# CREAR OFERTA
# ============================================
@router.post("/create_offer")
async def create_offer(offer: InternshipOffer):
    """Crear una nueva oferta de pasantía"""
    return offers_controller.create_offer(offer)

# ============================================
# OBTENER TODAS LAS OFERTAS
# ============================================
@router.get("/get_offers")
async def get_offers():
    """Obtener todas las ofertas de pasantía"""
    return offers_controller.get_offers()

# ============================================
# OBTENER OFERTA POR ID
# ============================================
@router.get("/get_offer/{offer_id}")
async def get_offer_by_id(offer_id: int):
    """Obtener una oferta específica por su ID"""
    return offers_controller.get_offer_by_id(offer_id)

# ============================================
# OBTENER OFERTAS POR EMPRESA
# ============================================
@router.get("/get_offers_by_company/{company_id}")
async def get_offers_by_company(company_id: int):
    """Obtener todas las ofertas de una empresa específica"""
    return offers_controller.get_offers_by_company(company_id)

# ============================================
# OBTENER OFERTAS DISPONIBLES (para estudiantes)
# ============================================
@router.get("/get_available_offers")
async def get_available_offers():
    """Obtener solo las ofertas disponibles (status = disponible y con vacantes)"""
    return offers_controller.get_available_offers()

# ============================================
# ACTUALIZAR OFERTA
# ============================================
@router.put("/update_offer/{offer_id}")
async def update_offer(offer_id: int, offer: InternshipOffer):
    """Actualizar una oferta existente"""
    return offers_controller.update_offer(offer_id, offer)

# ============================================
# ELIMINAR OFERTA
# ============================================
@router.delete("/delete_offer/{offer_id}")
async def delete_offer(offer_id: int):
    """Eliminar una oferta"""
    return offers_controller.delete_offer(offer_id)