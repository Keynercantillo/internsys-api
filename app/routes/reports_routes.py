from fastapi import APIRouter, HTTPException
from controllers.reports_controller import ReportsController
from models.report_model import Report

router = APIRouter()

reports_controller = ReportsController()

@router.post("/create_report")
async def create_report(report: Report):
    rpta = reports_controller.create_report(report)
    return rpta

@router.get("/get_report/{report_id}", response_model=Report)
async def get_report(report_id: int):
    rpta = reports_controller.get_report(report_id)
    return rpta

@router.get("/get_reports/")
async def get_reports():
    rpta = reports_controller.get_reports()
    return rpta

@router.get("/get_reports_by_type/{report_type}")
async def get_reports_by_type(report_type: str):
    rpta = reports_controller.get_reports_by_type(report_type)
    return rpta

@router.put("/update_report/{report_id}")
async def update_report(report_id: int, report: Report):
    rpta = reports_controller.update_report(report_id, report)
    return rpta

@router.delete("/delete_report/{report_id}")
async def delete_report(report_id: int):
    rpta = reports_controller.delete_report(report_id)
    return rpta