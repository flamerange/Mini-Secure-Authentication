from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, database, auth, dependencies
import jwt
from typing import Optional
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

load_dotenv()

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Mini Secure Authentication Server")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["localhost", "127.0.0.1", "*.render.com"])

templates = Jinja2Templates(directory="templates")


# --- HTML Routes ---

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

# --- API Routes ---

@app.post("/register")
@limiter.limit("5/minute")
async def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    db: Session = Depends(database.get_db)
):

    if role not in ["user", "admin"]:
        role = "user"
    
    hashed_password = auth.get_password_hash(password)
    db_user = models.User(username=username, email=email, hashed_password=hashed_password, role=role)
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"success": True, "message": "User successfully registered"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or Email already registered")

@app.post("/login")
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):

    # Authenticate by email
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@app.post("/refresh")
async def refresh_token(refresh_token: str = Form(...), db: Session = Depends(database.get_db)):
    try:
        payload = jwt.decode(refresh_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
        
    new_access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": new_access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout(token: str = Depends(dependencies.oauth2_scheme)):
    auth.blacklist_token(token)
    return {"message": "Successfully logged out"}

@app.get("/protected-data")


async def get_protected_data(current_user: models.User = Depends(dependencies.get_current_user)):
    return {
        "message": "This is protected data. You have access!",
        "user_id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }

@app.get("/admin-only")
async def get_admin_data(current_admin: models.User = Depends(dependencies.get_current_admin)):
    return {
        "message": "Welcome Admin! You have elevated privileges.",
        "admin_id": current_admin.id
    }

@app.get("/admin/users-list")
async def get_all_users_list(
    db: Session = Depends(database.get_db),
    current_admin: models.User = Depends(dependencies.get_current_admin)
):
    users = db.query(models.User).all()
    return [{"id": u.id, "username": u.username, "email": u.email, "role": u.role} for u in users]

@app.get("/admin/users", response_class=HTMLResponse)
async def admin_users_page(request: Request):
    return templates.TemplateResponse("admin_users.html", {"request": request})

if __name__ == "__main__":

    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
