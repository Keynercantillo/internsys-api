# routes/main_router.py
from fastapi import APIRouter
from routes import (
    students_routes,
    companies_routes,
    tutors_routes,
    internship_offers_routes,
    internship_assignments_routes,
    users_routes,
    agreements_routes,
    followup_visits_routes,
    reports_routes,
    evaluations_routes,
    notifications_routes
)

main_router = APIRouter()

main_router.include_router(students_routes.router, prefix="/api/v1", tags=["Students"])
main_router.include_router(companies_routes.router, prefix="/api/v1", tags=["Companies"])
main_router.include_router(tutors_routes.router, prefix="/api/v1", tags=["Tutors"])
main_router.include_router(internship_offers_routes.router, prefix="/api/v1", tags=["Internship Offers"])
main_router.include_router(internship_assignments_routes.router, prefix="/api/v1", tags=["Internship Assignments"])
main_router.include_router(users_routes.router, prefix="/api/v1", tags=["Users"])
main_router.include_router(agreements_routes.router, prefix="/api/v1", tags=["Agreements"])
main_router.include_router(followup_visits_routes.router, prefix="/api/v1", tags=["Follow-up Visits"])
main_router.include_router(reports_routes.router, prefix="/api/v1", tags=["Reports"])
main_router.include_router(evaluations_routes.router, prefix="/api/v1", tags=["Evaluations"])
main_router.include_router(notifications_routes.router, prefix="/api/v1", tags=["Notifications"])