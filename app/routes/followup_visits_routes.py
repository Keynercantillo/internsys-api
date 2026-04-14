from fastapi import APIRouter, HTTPException
from controllers.followup_visits_controller import FollowupVisitsController
from models.followup_visit_model import FollowupVisit

router = APIRouter()

followup_visits_controller = FollowupVisitsController()

@router.post("/create_followup_visit")
async def create_followup_visit(followup_visit: FollowupVisit):
    rpta = followup_visits_controller.create_followup_visit(followup_visit)
    return rpta

@router.get("/get_followup_visit/{visit_id}", response_model=FollowupVisit)
async def get_followup_visit(visit_id: int):
    rpta = followup_visits_controller.get_followup_visit(visit_id)
    return rpta

@router.get("/get_followup_visits/")
async def get_followup_visits():
    rpta = followup_visits_controller.get_followup_visits()
    return rpta

@router.get("/get_visits_by_assignment/{assignment_id}")
async def get_visits_by_assignment(assignment_id: int):
    rpta = followup_visits_controller.get_visits_by_assignment(assignment_id)
    return rpta

@router.put("/update_followup_visit/{visit_id}")
async def update_followup_visit(visit_id: int, followup_visit: FollowupVisit):
    rpta = followup_visits_controller.update_followup_visit(visit_id, followup_visit)
    return rpta

@router.delete("/delete_followup_visit/{visit_id}")
async def delete_followup_visit(visit_id: int):
    rpta = followup_visits_controller.delete_followup_visit(visit_id)
    return rpta