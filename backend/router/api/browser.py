
import os, random, uuid

from fastapi import APIRouter
from app.controller.browser.proxyController import ProxyController
from utility.response_config import json_response
from app.schemas.proxy import ProxyCheckRequest

router = APIRouter(prefix="/api/browsers", tags=["Browser Management"])

# Initialize the ProxyController
proxy_controller = ProxyController()

@router.post("/proxy-status", response_model=dict)
async def proxy_status(data: ProxyCheckRequest):
    proxy_data = await proxy_controller.check_proxy_status(data)
    return proxy_data




