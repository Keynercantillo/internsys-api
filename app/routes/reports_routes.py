from fastapi import APIRouter, HTTPException
from controllers.reports_controller import *
from models.report_model import Report

router = APIRouter()

nuevo_report = ReportsController()

@router.post("/create_report")
async def create_report(report: Report):
    rpta = nuevo_report.create_report(report)
    return rpta

@router.get("/get_report/{report_id}", response_model=Report)
async def get_report(report_id: int):
    rpta = nuevo_report.get_report(report_id)
    return rpta

@router.get("/get_reports/")
async def get_reports():
    rpta = nuevo_report.get_reports()
    return rpta

@router.get("/get_reports_by_assignment/{assignment_id}")
async def get_reports_by_assignment(assignment_id: int):
    rpta = nuevo_report.get_reports_by_assignment(assignment_id)
    return rpta

@router.get("/get_reports_by_student/{student_id}")
async def get_reports_by_student(student_id: int):
    rpta = nuevo_report.get_reports_by_student(student_id)
    return rpta

@router.put("/update_report/{report_id}")
async def update_report(report_id: int, report: Report):
    rpta = nuevo_report.update_report(report_id, report)
    return rpta

@router.delete("/delete_report/{report_id}")
async def delete_report(report_id: int):
    rpta = nuevo_report.delete_report(report_id)
    return rpta