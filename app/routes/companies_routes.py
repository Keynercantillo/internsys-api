from fastapi import APIRouter, HTTPException
from controllers.companies_controller import *
from models.company_model import Company

router = APIRouter()

nueva_company = CompaniesController()

@router.post("/create_company")
async def create_company(company: Company):
    rpta = nueva_company.create_company(company)
    return rpta

@router.get("/get_company/{company_id}", response_model=Company)
async def get_company(company_id: int):
    rpta = nueva_company.get_company(company_id)
    return rpta

@router.get("/get_companies/")
async def get_companies():
    rpta = nueva_company.get_companies()
    return rpta

@router.put("/update_company/{company_id}")
async def update_company(company_id: int, company: Company):
    rpta = nueva_company.update_company(company_id, company)
    return rpta

@router.delete("/delete_company/{company_id}")
async def delete_company(company_id: int):
    rpta = nueva_company.delete_company(company_id)
    return rpta