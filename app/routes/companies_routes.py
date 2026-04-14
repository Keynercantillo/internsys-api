from fastapi import APIRouter, HTTPException
from controllers.companies_controller import CompaniesController
from models.company_model import Company

router = APIRouter()
companies_controller = CompaniesController()


@router.post("/create_company")
async def create_company(company: Company):
    """Crear una nueva empresa"""
    rpta = companies_controller.create_company(company)
    return rpta


@router.get("/get_company/{company_id}", response_model=Company)
async def get_company(company_id: int):
    """Obtener empresa por ID"""
    rpta = companies_controller.get_company(company_id)
    return rpta


@router.get("/get_companies/")
async def get_companies():
    """Obtener todas las empresas"""
    rpta = companies_controller.get_companies()
    return rpta


@router.get("/get_companies_by_sector/{sector}")
async def get_companies_by_sector(sector: str):
    """Obtener empresas por sector"""
    rpta = companies_controller.get_companies_by_sector(sector)
    return rpta


@router.get("/get_company_by_user/{user_id}")
async def get_company_by_user(user_id: int):
    """Obtener empresa asociada a un usuario"""
    rpta = companies_controller.get_company_by_user(user_id)
    return rpta


@router.put("/update_company/{company_id}")
async def update_company(company_id: int, company: Company):
    """Actualizar empresa"""
    rpta = companies_controller.update_company(company_id, company)
    return rpta


@router.delete("/delete_company/{company_id}")
async def delete_company(company_id: int):
    """Eliminar empresa"""
    rpta = companies_controller.delete_company(company_id)
    return rpta