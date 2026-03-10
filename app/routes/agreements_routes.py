from fastapi import APIRouter, HTTPException
from controllers.agreements_controller import *
from models.agreement_model import Agreement

router = APIRouter()

nuevo_agreement = AgreementsController()

@router.post("/create_agreement")
async def create_agreement(agreement: Agreement):
    rpta = nuevo_agreement.create_agreement(agreement)
    return rpta

@router.get("/get_agreement/{agreement_id}", response_model=Agreement)
async def get_agreement(agreement_id: int):
    rpta = nuevo_agreement.get_agreement(agreement_id)
    return rpta

@router.get("/get_agreements/")
async def get_agreements():
    rpta = nuevo_agreement.get_agreements()
    return rpta

@router.get("/get_agreements_by_company/{company_id}")
async def get_agreements_by_company(company_id: int):
    rpta = nuevo_agreement.get_agreements_by_company(company_id)
    return rpta

@router.get("/get_active_agreements/")
async def get_active_agreements():
    rpta = nuevo_agreement.get_active_agreements()
    return rpta

@router.put("/update_agreement/{agreement_id}")
async def update_agreement(agreement_id: int, agreement: Agreement):
    rpta = nuevo_agreement.update_agreement(agreement_id, agreement)
    return rpta

@router.delete("/delete_agreement/{agreement_id}")
async def delete_agreement(agreement_id: int):
    rpta = nuevo_agreement.delete_agreement(agreement_id)
    return rpta