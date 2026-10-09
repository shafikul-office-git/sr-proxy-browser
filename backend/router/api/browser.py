
import os, random

from fastapi import APIRouter, Depends, Request
from app.models import BrowserInfo, BrowserConfig
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, model_validator
from utility.proxy_status import check_proxy_status
from app.controller.browser.open_browser import open_browser
from app.controller.browser.browserController import open_browser_playwright
from utility.helper_function import (
    build_fingerprint,
    get_languages,
    get_timezone_from_ip,
    is_value_exists,
    get_random_free_port,
    hash_password,
    verify_password,
)
from app.database import get_db
import uuid

router = APIRouter(
    prefix="/api/browsers",
    tags=["browsers"]
)

def return_json_response(data: dict, status_code: int = 200, message: str = "Success", status: str = "success"):
    return {"data": data, "status_code": status_code, "message": message, "status": status}

class BrowserValidation(BaseModel):
    profile_name: str
    browser_port: int = Field(ge=1024, le=49151, description="Browser port must be between 1024 and 49151")
    proxy_host: str | None = None
    proxy_port: int | None = None
    proxy_username: str | None = None
    proxy_password: str | None = None
    proxy_country: str | None = None
    proxy_city: str | None = None
    protected: bool = False
    protected_password: str | None = None
    proxy_type: str = "http" # https, http, socks5

    @model_validator(mode="after")
    def check_password(self):
        if self.protected and not self.protected_password:
            raise ValueError("protected_password is required when protected=True")
        return self


class PasswordPayload(BaseModel):
    password: str = Field(min_length=6, description="Browser protection password")


class PasswordVerifyPayload(BaseModel):
    current_password: str = Field(min_length=6, description="Current browser password")


class PasswordResetPayload(BaseModel):
    current_password: str = Field(min_length=6, description="Current browser password")
    new_password: str = Field(min_length=6, description="New browser password")


def _browser_safe_data(browser: BrowserInfo, db: Session) -> dict:
    browser_conf = (
        db.query(BrowserConfig.ip_info)
        .filter(BrowserConfig.browser_info_id == browser.id)
        .first()
    )

    ip_info = browser_conf[0] if browser_conf else None

    return {
        "id": browser.id,
        "profile_name": browser.profile_name,
        "folder_name": browser.folder_name,
        "browser_port": browser.browser_port,
        "proxy_type": browser.proxy_type,
        "proxy_host": browser.proxy_host,
        "proxy_port": browser.proxy_port,
        "proxy_username": browser.proxy_username,
        "proxy_password": browser.proxy_password,
        "proxy_country": browser.proxy_country,
        "proxy_city": browser.proxy_city,
        "protected": browser.protected,
        "status": browser.status,
        "created_at": browser.created_at,
        "ip_info": ip_info,
        "proxy_status": browser.proxy_status
    }


@router.get("/find-port")
async def find_available_port(db: Session = Depends(get_db)):
    existing_ports = {browser.browser_port for browser in db.query(BrowserInfo).all()}
    port = get_random_free_port()
    while port in existing_ports:
        port = get_random_free_port()
    return return_json_response({"available_port": port}, message="Available port found successfully", status="success", status_code=200)

@router.get("/")
def get_all_browsers(db: Session = Depends(get_db)):
    browsers = db.query(BrowserInfo).order_by(BrowserInfo.created_at.desc()).all()

    return return_json_response({"browsers": [_browser_safe_data(browser, db) for browser in browsers]}, message="Browsers retrieved successfully", status="success", status_code=200)

@router.post("/create")
def create_browser_profile(request: Request, payload: BrowserValidation, db: Session = Depends(get_db)):
    folder_name = uuid.uuid4().hex[:13]
    check_folder_name_in_db = is_value_exists(db, BrowserInfo, BrowserInfo.folder_name, folder_name)
    while check_folder_name_in_db:
        folder_name = uuid.uuid4().hex[:13]
        check_folder_name_in_db = is_value_exists(db, BrowserInfo, BrowserInfo.folder_name, folder_name)

    check_browser_port_in_db = is_value_exists(db, BrowserInfo, BrowserInfo.browser_port, payload.browser_port)
    if check_browser_port_in_db:
        return return_json_response({}, status_code=400, message="Browser port already exists. Please choose a different port.", status="error")

    # =========================
    # Check Proxy status
    # =========================
    check_status = check_proxy_status(payload.proxy_host, payload.proxy_port, payload.proxy_username, payload.proxy_password, payload.proxy_type) if payload.proxy_host and payload.proxy_port else True
    print(f"Proxy status: {'Working' if check_status else 'Not Working'}")

    # ===================
    # Insert In DB browser data
    # ====================
    new_browser_info = BrowserInfo(
        profile_name=payload.profile_name,
        folder_name=folder_name,
        proxy_status=check_status,
        browser_port=payload.browser_port,
        proxy_host=payload.proxy_host,
        proxy_port=payload.proxy_port,
        proxy_username=payload.proxy_username,
        proxy_password=payload.proxy_password,
        proxy_country=payload.proxy_country,
        proxy_city=payload.proxy_city,
        proxy_type=payload.proxy_type,
        protected=payload.protected,
        protected_password=hash_password(payload.protected_password) if payload.protected else None,
    )
    db.add(new_browser_info)
    db.flush() # <-- Flush pushes the record to DB to generate 'new_browser_info.id' without committing the transaction yet.

    # ===================
    # Insert In DB browser config data with default fingerprint (will update after open browser and get real fingerprint)
    # ====================
    ip_info = get_timezone_from_ip(payload.proxy_host or request.client.host)
    fingerprint = build_fingerprint()
    lang_data = get_languages(ip_info.get("countryCode"))

    config_data = BrowserConfig(
        browser_info_id=new_browser_info.id,
        ip_info= ip_info,
        window_width=fingerprint['width'],
        window_height=fingerprint['height'],
        user_agent=fingerprint['user_agent'],
        browser_language=lang_data["language"],
        browser_languages=lang_data["languages"],
        hardware_concurrency=fingerprint['hardware_concurrency'],
        device_memory=fingerprint['device_memory'],
        webgl_vendor=fingerprint['webgl_vendor'],
        webgl_renderer=fingerprint['webgl_renderer'],
        chrome_version= fingerprint['chrome_version'],
        browser_font=lang_data['fonts'],
        canvas_noise={"r": random.randint(1, 10), "g": random.randint(1, 10), "b": random.randint(1, 10), "a": random.randint(1, 10)} 
    )
    db.add(config_data)
    db.commit()

    db.refresh(new_browser_info)
    db.refresh(config_data)

    return return_json_response({ "browserinfo": new_browser_info , "config": config_data}, message="Browser profile created successfully.", status="success", status_code=200)

@router.put("/update/{browser_id}")
def update_browser_profile(
    browser_id: int,
    payload: BrowserValidation,
    db: Session = Depends(get_db)
):

    browser = db.query(BrowserInfo).filter(BrowserInfo.id == browser_id).first()

    if not browser:
        return return_json_response(
            {},
            status_code=404,
            message="Browser not found",
            status="error"
        )

    # protected validation already handled by Pydantic

    browser.profile_name = payload.profile_name

    browser.proxy_host = payload.proxy_host
    browser.proxy_port = payload.proxy_port
    browser.proxy_username = payload.proxy_username
    browser.proxy_password = payload.proxy_password
    browser.proxy_country = payload.proxy_country
    browser.proxy_city = payload.proxy_city
    browser.proxy_type = payload.proxy_type
    browser.protected = payload.protected
    if payload.protected:
        if payload.protected_password:
            browser.protected_password = hash_password(payload.protected_password)
    else:
        browser.protected_password = None

    db.commit()
    db.refresh(browser)

    return return_json_response(
        _browser_safe_data(browser, db),
        message="Browser profile updated successfully",
        status="success",
        status_code=200
    )


@router.post("/password/add/{browser_id}")
def add_browser_password(browser_id: int, payload: PasswordPayload, db: Session = Depends(get_db)):
    browser = db.query(BrowserInfo).filter(BrowserInfo.id == browser_id).first()
    if not browser:
        return return_json_response({}, status_code=404, message="Browser not found", status="error")

    if browser.protected:
        return return_json_response({}, status_code=400, message="Browser already has a password.", status="error")

    browser.protected = True
    browser.protected_password = hash_password(payload.password)
    db.commit()
    db.refresh(browser)

    return return_json_response(
        {"browserinfo": _browser_safe_data(browser, db)},
        message="Password added successfully.",
        status="success",
        status_code=200,
    )


@router.post("/password/remove/{browser_id}")
def remove_browser_password(browser_id: int, payload: PasswordVerifyPayload, db: Session = Depends(get_db)):
    browser = db.query(BrowserInfo).filter(BrowserInfo.id == browser_id).first()
    if not browser:
        return return_json_response({}, status_code=404, message="Browser not found", status="error")

    if not browser.protected:
        return return_json_response({}, status_code=400, message="Browser is not password protected.", status="error")

    if not verify_password(payload.current_password, browser.protected_password or ""):
        return return_json_response({}, status_code=403, message="Incorrect password. Browser cannot be removed.", status="error")

    browser.protected = False
    browser.protected_password = None
    db.commit()
    db.refresh(browser)

    return return_json_response(
        {"browserinfo": _browser_safe_data(browser, db)},
        message="Password protection removed successfully.",
        status="success",
        status_code=200,
    )


@router.post("/password/forget/{browser_id}")
def forget_browser_password(browser_id: int, payload: PasswordResetPayload, db: Session = Depends(get_db)):
    browser = db.query(BrowserInfo).filter(BrowserInfo.id == browser_id).first()
    if not browser:
        return return_json_response({}, status_code=404, message="Browser not found", status="error")

    if not browser.protected:
        return return_json_response({}, status_code=400, message="Browser is not password protected.", status="error")

    if not verify_password(payload.current_password, browser.protected_password or ""):
        return return_json_response({}, status_code=403, message="Incorrect current password. Cannot reset password.", status="error")

    browser.protected_password = hash_password(payload.new_password)
    db.commit()
    db.refresh(browser)

    return return_json_response(
        {"browserinfo": _browser_safe_data(browser, db)},
        message="Password reset successfully.",
        status="success",
        status_code=200,
    )


@router.delete("/delete/{browser_id}")
def delete_browser_profile(
    browser_id: int,
    password: str | None = None,
    db: Session = Depends(get_db)
):

    browser = db.query(BrowserInfo).filter(BrowserInfo.id == browser_id).first()
    
    if not browser:
        return return_json_response(
            {},
            status_code=404,
            message="Browser not found",
            status="error"
        )

    if browser.protected:
        if not password or not verify_password(password, browser.protected_password or ""):
            return return_json_response(
                {},
                status_code=403,
                message="Browser is protected. Correct password required to delete.",
                status="error"
            )

    # Delete dependent records explicitly to ensure cleanup even if DB-level
    # ON DELETE CASCADE isn't enforced (e.g., SQLite without PRAGMA foreign_keys=ON)
    try:
        db.query(BrowserConfig).filter(BrowserConfig.browser_info_id == browser_id).delete(synchronize_session=False)
    except Exception:
        # if something goes wrong, continue to attempt deleting the browser object
        pass

    db.delete(browser)
    db.commit()

    profile_path = "C:\\LocalChromeProfiles" 
    folder_name = browser.folder_name
    folder_path = os.path.join(profile_path, folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        try:
            # Remove the entire folder and its contents
            import shutil
            shutil.rmtree(folder_path)
        except Exception as e:
            # Log the error but don't fail the API response since the DB record is already deleted
            print(f"Error deleting browser profile folder: {e}")

    return return_json_response(
        {},
        message="Browser profile deleted successfully",
        status="success",
        status_code=200
    )


def _verify_browser_access(browser: BrowserInfo, password: str | None):
    if not browser.protected:
        return True
    return bool(password and verify_password(password, browser.protected_password or ""))


# ------------
# open browser with local chorme browser
# ------------------------
@router.get("/open/{browser_id}")
def open_browser_profile(browser_id: int, password: str | None = None, db: Session = Depends(get_db)):
    browser = db.query(BrowserInfo).filter(BrowserInfo.id == browser_id).first()

    if not browser:
        return return_json_response(
            {},
            status_code=404,
            message="Browser not found",
            status="error"
        )

    if not _verify_browser_access(browser, password):
        return return_json_response(
            {},
            status_code=403,
            message="Browser is password protected. Correct password required to open.",
            status="error"
        )

    profile_path = "C:\\LocalChromeProfiles"  # Change this to your desired base path for Chrome profiles
    profile_path = f"{profile_path}\\{browser.folder_name}"
    os.makedirs(profile_path, exist_ok=True)

    # Call the open_browser function with the required parameters
    proxy_info = {
        "proxy_username": browser.proxy_username,
        "proxy_password": browser.proxy_password,
        "proxy_host": browser.proxy_host,
        "proxy_port": browser.proxy_port,
        "proxy_country": browser.proxy_country,
        "proxy_city": browser.proxy_city
    }
    result = open_browser(debug_port=browser.browser_port, profile_path=profile_path, proxy_info=proxy_info)
    return return_json_response({'browser_result': result, 'proxy_info': proxy_info}, message="Browser opened successfully", status="success", status_code=200)

# ------------------------
# open browser with selenium (for better proxy support and WebRTC leak protection)
# ------------------------
@router.get('/open/selenium/{browser_id}')
async def open_browser_with_selenium(browser_id: int, password: str | None = None, db: Session = Depends(get_db)):
    browser = db.query(BrowserInfo).filter(BrowserInfo.id == browser_id).first()

    if not browser:
        return return_json_response(
            {},
            status_code=404,
            message="Browser not found",
            status="error"
        )

    if not _verify_browser_access(browser, password):
        return return_json_response(
            {},
            status_code=403,
            message="Browser is password protected. Correct password required to open.",
            status="error"
        )

    profile_path = "C:\\LocalChromeProfiles"  # Change this to your desired base path for Chrome profiles
    profile_path = f"{profile_path}\\{browser.folder_name}"
    os.makedirs(profile_path, exist_ok=True)

    # Call the open_browser function with the required parameters
    proxy_info = {
        "proxy_username": browser.proxy_username,
        "proxy_password": browser.proxy_password,
        "proxy_host": browser.proxy_host,
        "proxy_port": browser.proxy_port,
        "proxy_country": browser.proxy_country,
        "proxy_city": browser.proxy_city
    }
    # https://browserleaks.com/webrtc
    browser_conf = db.query(BrowserConfig).filter(BrowserConfig.browser_info_id == browser_id).first()
    if not browser_conf:
        return {"status": "error", "message": "Browser configuration not found."}
    
    result = await open_browser_playwright(debug_port=browser.browser_port, profile_path=profile_path, proxy_info=proxy_info, proxy_type=browser.proxy_type, browser_conf=browser_conf)    
    return return_json_response({'browser_result': result, 'proxy_info': proxy_info}, message="Browser opened successfully", status="success", status_code=200)

