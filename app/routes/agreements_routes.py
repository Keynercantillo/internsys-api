from fastapi import APIRouter, HTTPException
from controllers.agreements_controller import AgreementsController
from models.agreement_model import Agreement

router = APIRouter()

agreements_controller = AgreementsController()

@router.post("/create_agreement")
async def create_agreement(agreement: Agreement):
    rpta = agreements_controller.create_agreement(agreement)
    return rpta

@router.get("/get_agreement/{agreement_id}", response_model=Agreement)
async def get_agreement(agreement_id: int):
    rpta = agreements_controller.get_agreement(agreement_id)
    return rpta

@router.get("/get_agreements/")
async def get_agreements():
    rpta = agreements_controller.get_agreements()
    return rpta

@router.get("/get_agreements_by_student/{student_id}")
async def get_agreements_by_student(student_id: int):
    rpta = agreements_controller.get_agreements_by_student(student_id)
    return rpta

@router.put("/update_agreement/{agreement_id}")
async def update_agreement(agreement_id: int, agreement: Agreement):
    rpta = agreements_controller.update_agreement(agreement_id, agreement)
    return rpta

@router.delete("/delete_agreement/{agreement_id}")
async def delete_agreement(agreement_id: int):
    rpta = agreements_controller.delete_agreement(agreement_id)
    return rpta