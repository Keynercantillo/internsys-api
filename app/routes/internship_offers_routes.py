from fastapi import APIRouter, HTTPException
from controllers.internship_offers_controller import *
from models.internship_offer_model import InternshipOffer

router = APIRouter()

nueva_offer = InternshipOffersController()

@router.post("/create_internship_offer")
async def create_internship_offer(offer: InternshipOffer):
    rpta = nueva_offer.create_offer(offer)
    return rpta

@router.get("/get_internship_offer/{offer_id}", response_model=InternshipOffer)
async def get_internship_offer(offer_id: int):
    rpta = nueva_offer.get_offer(offer_id)
    return rpta

@router.get("/get_internship_offers/")
async def get_internship_offers():
    rpta = nueva_offer.get_offers()
    return rpta

@router.get("/get_internship_offers_by_company/{company_id}")
async def get_internship_offers_by_company(company_id: int):
    rpta = nueva_offer.get_offers_by_company(company_id)
    return rpta

@router.put("/update_internship_offer/{offer_id}")
async def update_internship_offer(offer_id: int, offer: InternshipOffer):
    rpta = nueva_offer.update_offer(offer_id, offer)
    return rpta

@router.delete("/delete_internship_offer/{offer_id}")
async def delete_internship_offer(offer_id: int):
    rpta = nueva_offer.delete_offer(offer_id)
    return rpta