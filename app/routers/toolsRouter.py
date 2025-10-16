# app/routers/toolsRouter.py
from fastapi import APIRouter
from app.routers.tools.menuToolsRouter import router as menuRouter
from app.routers.tools.orderToolsRouter import router as orderRouter
from app.routers.tools.recommendationRouter import router as recommendationsRouter

router = APIRouter(prefix="/api/tools", tags=["tools"])

@router.get("/greet")
def greet():
    return {"message": "[[SAY]]Welcome to the Cheesy Chazz Pizza Ordering Hotline! Please provide me with your name and phone number sothet we can take your order.[[/SAY]]"}

# Mount feature-specific routers
router.include_router(menuRouter)
router.include_router(orderRouter)
router.include_router(recommendationsRouter)
