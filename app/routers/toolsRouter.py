# app/routers/toolsRouter.py
from fastapi import APIRouter
from app.routers.tools.menuToolsRouter import router as menuRouter
from app.routers.tools.orderToolsRouter import router as orderRouter

router = APIRouter(prefix="/api/tools", tags=["tools"])

@router.get("/greet")
def greet():
    return {"message": "[[SAY]]Welcome to Cheesy Chazz Pizza! How can I help you today?[[/SAY]]"}

# Mount feature-specific routers
router.include_router(menuRouter)
router.include_router(orderRouter)
