from fastapi import APIRouter, HTTPException
from controllers.internship_offers_controller import InternshipOfferController
from models.internship_offers_model import InternshipOffer

router = APIRouter()
offers_controller = InternshipOfferController()


@router.post("/create_offer")
async def create_offer(offer: InternshipOffer):
    rpta = offers_controller.create_offer(offer)
    return rpta


@router.get("/get_offer/{offer_id}")
async def get_offer(offer_id: int):
    rpta = offers_controller.get_offer(offer_id)
    return rpta


@router.get("/get_offers/")
async def get_offers():
    rpta = offers_controller.get_offers()
    return rpta


@router.get("/get_offers_by_company/{company_id}")
async def get_offers_by_company(company_id: int):
    rpta = offers_controller.get_offers_by_company(company_id)
    return rpta


@router.put("/update_offer/{offer_id}")
async def update_offer(offer_id: int, offer: InternshipOffer):
    rpta = offers_controller.update_offer(offer_id, offer)
    return rpta


@router.delete("/delete_offer/{offer_id}")
async def delete_offer(offer_id: int):
    rpta = offers_controller.delete_offer(offer_id)
    return rpta