
from config.app import app, templates, os, Request,HTMLResponse,RedirectResponse
from fastapi import Form,Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.users import User
from utility.helper_function import hash_password, verify_password
import random, uuid

@app.get('/login', response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/auth/login.html",
        context={"request": request, "version": os.getenv("APP_VERSION")}
    )

@app.post('/login')
async def logged_in(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    form_data = {
        "email": email
    }

    # 1) user find by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return templates.TemplateResponse("pages/auth/login.html", {
            "request": request,
            "error": "Invalid email or password",
            "form_data": form_data
        })

    # 3) password verify (argon2 / passlib)
    if not verify_password(password, user.password):
        return templates.TemplateResponse("pages/auth/login.html", {
            "request": request,
            "error": "Invalid email or password",
            "form_data": form_data
        })

    # 4) session set
    request.session["user"] = {"username": user.username, "name": user.name}

    # 5) redirect
    return RedirectResponse("/dashboard", status_code=302)

@app.get('/signup', response_class=HTMLResponse)
def registater(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="pages/auth/registater.html",
        context={"request": request, "version": os.getenv("APP_VERSION")}
    )

@app.post('/signup')
async def signup(
    request: Request, 
    name:str = Form(...),
    email:str = Form(...),
    password:str = Form(...),
    re_password:str = Form(...),
    db: Session = Depends(get_db)
    ):
    form_data = {
        "name": name,
        "email": email
    }

    # 1) password match
    if password != re_password:
        return templates.TemplateResponse("pages/auth/registater.html", {
            "request": request,
            "error": "Passwords do not match",
            "form_data": form_data
        })

    # 2) email exists
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("pages/auth/registater.html", {
            "request": request,
            "error": "Email already registered",
            "form_data": form_data
        })

    # username generate
    username = f"{uuid.uuid4()}_{random.randint(33,9999)}"

    # 3) hash password
    hashed = hash_password(password)

    # 4) create user
    user = User(
        username=username,
        name=name,
        email=email,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # 5) session login
    request.session["user"] = {"username": user.username, "name": name}

    return RedirectResponse("/dashboard", status_code=302)

@app.get('/logout')
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=302)

@app.get('/dashboard', response_class=HTMLResponse)
def dashboard(request: Request,db: Session = Depends(get_db)):
    users = db.query(User).all()

    return templates.TemplateResponse(
        request=request,
        name="pages/authenticated/dashboard.html",
        context={
            "request": request,
            "version": os.getenv("APP_VERSION"),
            "users": users 
        }
    )

