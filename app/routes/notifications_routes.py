from fastapi import APIRouter, HTTPException
from controllers.notifications_controller import NotificationsController
from models.notification_model import Notification

router = APIRouter()

notifications_controller = NotificationsController()

@router.post("/create_notification")
async def create_notification(notification: Notification):
    rpta = notifications_controller.create_notification(notification)
    return rpta

@router.get("/get_notification/{notification_id}", response_model=Notification)
async def get_notification(notification_id: int):
    rpta = notifications_controller.get_notification(notification_id)
    return rpta

@router.get("/get_notifications/")
async def get_notifications():
    rpta = notifications_controller.get_notifications()
    return rpta

@router.get("/get_notifications_by_user/{user_id}")
async def get_notifications_by_user(user_id: int):
    rpta = notifications_controller.get_notifications_by_user(user_id)
    return rpta

@router.put("/update_notification/{notification_id}")
async def update_notification(notification_id: int, notification: Notification):
    rpta = notifications_controller.update_notification(notification_id, notification)
    return rpta

@router.delete("/delete_notification/{notification_id}")
async def delete_notification(notification_id: int):
    rpta = notifications_controller.delete_notification(notification_id)
    return rpta