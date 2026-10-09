from fastapi import APIRouter
from app.controller.browser.browserController import BrowserController
from app.schemas.browser import ProfileCheckRequest

router = APIRouter(prefix="/api/browser", tags=["Browser Management"])

# Initialize the ProxyController
browser_controller = BrowserController()

@router.post("/add/profile", response_model=dict)
async def add_profile(data: ProfileCheckRequest):
    result = await browser_controller.add_profile(data)
    return result

