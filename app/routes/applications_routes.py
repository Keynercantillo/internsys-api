from fastapi import APIRouter, HTTPException
from controllers.applications_controller import ApplicationsController
from models.applications_model import Application

router = APIRouter()
applications_controller = ApplicationsController()

@router.post("/create_application")
async def create_application(application: Application):
    return applications_controller.create_application(application)

@router.get("/get_applications/")
async def get_applications():
    return applications_controller.get_applications()

@router.get("/get_applications_by_company/{empresa_id}")
async def get_applications_by_company(empresa_id: int):
    return applications_controller.get_applications_by_company(empresa_id)

@router.put("/update_application_status/{application_id}")
async def update_application_status(application_id: int, status: str, tutor_id: int = None):
    return applications_controller.update_application_status(application_id, status, tutor_id)

@router.delete("/delete_application/{application_id}")
async def delete_application(application_id: int):
    return applications_controller.delete_application(application_id)