
import os, random, uuid

from fastapi import APIRouter
from app.controller.browser.proxyController import ProxyController
from utility.response_config import json_response
from app.schemas.proxy import ProxyCheckRequest

router = APIRouter(prefix="/api/browsers", tags=["Browser Management"])

# Initialize the ProxyController
proxy_controller = ProxyController()


@router.get("/proxy")
async def get_proxies():
    proxy_list = """
31.59.20.176:6754:fkuoneku:4i6n46x80ra4
45.38.107.97:6014:fkuoneku:4i6n46x80ra4
64.137.96.74:6641:fkuoneku:4i6n46x80ra4
198.23.243.226:6361:fkuoneku:4i6n46x80ra4
38.154.185.97:6370:fkuoneku:4i6n46x80ra4
84.247.60.125:6095:fkuoneku:4i6n46x80ra4
142.111.67.146:5611:fkuoneku:4i6n46x80ra4
191.96.254.138:6185:fkuoneku:4i6n46x80ra4
31.58.9.4:6077:fkuoneku:4i6n46x80ra4
198.46.161.42:5092:fkuoneku:4i6n46x80ra4
"""
    proxies = [
        line.strip()
        for line in proxy_list.strip().splitlines()
        if line.strip()
    ]
    return {"data": proxies}


@router.post("/proxy-status", response_model=dict)
async def proxy_status(data: ProxyCheckRequest):
    proxy_data = await proxy_controller.check_proxy_status(data)
    return proxy_data



