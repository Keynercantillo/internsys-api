from fastapi import APIRouter, HTTPException
from controllers.profiles_controller import ProfilesController
from models.profile_model import Profile

router = APIRouter()

profiles_controller = ProfilesController()

@router.post("/create_profile")
async def create_profile(profile: Profile):
    rpta = profiles_controller.create_profile(profile)
    return rpta

@router.get("/get_profile/{profile_id}", response_model=Profile)
async def get_profile(profile_id: int):
    rpta = profiles_controller.get_profile(profile_id)
    return rpta

@router.get("/get_profiles/")
async def get_profiles():
    rpta = profiles_controller.get_profiles()
    return rpta

@router.get("/get_profile_by_user/{user_id}")
async def get_profile_by_user(user_id: int):
    rpta = profiles_controller.get_profile_by_user(user_id)
    return rpta

@router.put("/update_profile/{profile_id}")
async def update_profile(profile_id: int, profile: Profile):
    rpta = profiles_controller.update_profile(profile_id, profile)
    return rpta

@router.delete("/delete_profile/{profile_id}")
async def delete_profile(profile_id: int):
    rpta = profiles_controller.delete_profile(profile_id)
    return rpta