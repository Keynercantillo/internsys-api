from fastapi import APIRouter, HTTPException
from controllers.followup_visits_controller import *
from models.followup_visit_model import FollowupVisit

router = APIRouter()

nueva_visit = FollowupVisitsController()

@router.post("/create_followup_visit")
async def create_followup_visit(visit: FollowupVisit):
    rpta = nueva_visit.create_visit(visit)
    return rpta

@router.get("/get_followup_visit/{visit_id}", response_model=FollowupVisit)
async def get_followup_visit(visit_id: int):
    rpta = nueva_visit.get_visit(visit_id)
    return rpta

@router.get("/get_followup_visits/")
async def get_followup_visits():
    rpta = nueva_visit.get_visits()
    return rpta

@router.get("/get_followup_visits_by_assignment/{assignment_id}")
async def get_followup_visits_by_assignment(assignment_id: int):
    rpta = nueva_visit.get_visits_by_assignment(assignment_id)
    return rpta

@router.get("/get_followup_visits_by_tutor/{tutor_id}")
async def get_followup_visits_by_tutor(tutor_id: int):
    rpta = nueva_visit.get_visits_by_tutor(tutor_id)
    return rpta

@router.put("/update_followup_visit/{visit_id}")
async def update_followup_visit(visit_id: int, visit: FollowupVisit):
    rpta = nueva_visit.update_visit(visit_id, visit)
    return rpta

@router.delete("/delete_followup_visit/{visit_id}")
async def delete_followup_visit(visit_id: int):
    rpta = nueva_visit.delete_visit(visit_id)
    return rpta