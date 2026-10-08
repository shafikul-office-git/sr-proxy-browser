
import os
from fastapi import FastAPI,Request,HTTPException
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from pathlib import Path
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

# =================================
# If login => block path || ex: '/login'
# =================================
@app.middleware("http")
async def already_loggedIn(request: Request, call_next):
    user = request.session.get("user") 
    blocked_paths = ["/login", "/signup"]

    if request.url.path in blocked_paths and user:
        return RedirectResponse("/dashboard", status_code=302)

    return await call_next(request)

# =================================
# If not login => block path  || ex: '/logout'
# =================================
@app.middleware("http")
async def protect_dashboard(request: Request, call_next):
    user = request.session.get("user")
    protected_paths = ["/dashboard", "/logout"]

    if request.url.path in protected_paths and not user:
        return RedirectResponse("/login", status_code=302)

    return await call_next(request)

# =================================
# Add Middleware Only Web er jonno.
# =================================
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "super-secret-key"),
    session_cookie="session",     
    max_age=60 * 60 * 24,          
    # https_only=True,   
)

# =================================
# Add Middleware API ROUTE
# =================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGIN", ["*"]).split(","),
    allow_credentials=True,
    allow_methods=os.getenv("ALLOW_METHODS", ["GET", "POST", "PUT", "DELETE"]).split(","),
    allow_headers=os.getenv("ALLOW_HEADERS", ["*"]).split(",")
)

# =================================
# Template Dir & Static Dir
# =================================
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

