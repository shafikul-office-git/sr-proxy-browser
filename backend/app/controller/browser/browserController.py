import random
import threading
import asyncio
import json
from playwright.sync_api import sync_playwright, BrowserContext, Page

class BrowserController:
    def __init__(self):
        pass

    async def add_profile(self, data):
        return {
            "status": True,
            "message": "Profile data validated successfully",
            "env": data.env,
            "form": data.form.model_dump(mode="json"),
            "proxy": data.proxy.model_dump(exclude={"password"}),
            "launch": data.launch,
            "message": "Success profile created"
        }