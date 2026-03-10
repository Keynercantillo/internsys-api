from fastapi import APIRouter, HTTPException
from controllers.notifications_controller import *
from models.notification_model import Notification

router = APIRouter()

nueva_notification = NotificationsController()

@router.post("/create_notification")
async def create_notification(notification: Notification):
    rpta = nueva_notification.create_notification(notification)
    return rpta

@router.get("/get_notification/{notification_id}", response_model=Notification)
async def get_notification(notification_id: int):
    rpta = nueva_notification.get_notification(notification_id)
    return rpta

@router.get("/get_notifications/")
async def get_notifications():
    rpta = nueva_notification.get_notifications()
    return rpta

@router.get("/get_notifications_by_user/{user_id}")
async def get_notifications_by_user(user_id: int):
    rpta = nueva_notification.get_notifications_by_user(user_id)
    return rpta

@router.get("/get_unread_notifications_by_user/{user_id}")
async def get_unread_notifications_by_user(user_id: int):
    rpta = nueva_notification.get_unread_notifications_by_user(user_id)
    return rpta

@router.put("/mark_notification_as_read/{notification_id}")
async def mark_notification_as_read(notification_id: int):
    rpta = nueva_notification.mark_as_read(notification_id)
    return rpta

@router.put("/mark_all_notifications_as_read/{user_id}")
async def mark_all_notifications_as_read(user_id: int):
    rpta = nueva_notification.mark_all_as_read(user_id)
    return rpta

@router.put("/update_notification/{notification_id}")
async def update_notification(notification_id: int, notification: Notification):
    rpta = nueva_notification.update_notification(notification_id, notification)
    return rpta

@router.delete("/delete_notification/{notification_id}")
async def delete_notification(notification_id: int):
    rpta = nueva_notification.delete_notification(notification_id)
    return rpta