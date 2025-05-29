from fastapi import APIRouter, Request, Response, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services import session_manager

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_post(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...)
):
    client_ip = request.client.host
    
    # Закрываем старые сессии
    sessions_to_remove = [
        session_id for session_id, data in session_manager.sessions.items()
        if data["ip_address"] == client_ip or data["username"] == username
    ]
    for session_id in sessions_to_remove:
        session_manager.close_session(session_id)
    
    # Создаем новую сессию
    session_id, error = session_manager.create_session(client_ip, username, password)
    if error:
        return {"status": "error", "msg": "Database authentication failed", "details": error}
    
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    return {"status": "ok", "msg": "Login successful", "session_id": session_id, "ip": client_ip}

@router.get("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    session_manager.close_session(session_id)
    response.delete_cookie("session_id")
    return RedirectResponse(url="/login", status_code=303)
