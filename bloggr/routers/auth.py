from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from sqlalchemy import schema
import sqlalchemy
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from werkzeug.security import generate_password_hash, check_password_hash

from bloggr.middleware import flash, get_flashed_messages

from ..templates import TemplateResponse
from ..db import get_db, schemas, models, crud

router = APIRouter(prefix='/auth')

@router.get('/register', response_class=HTMLResponse)
async def register(request: Request, 
             username: str | None = Form(None)):
    
    content = {'request': request}
    content['messages'] = get_flashed_messages(request)

    return TemplateResponse('auth/register.html', content)


@router.post('/register')
def register(request: Request,
             username: str | None = Form(None), 
             password: str | None = Form(None),
             db: Session = Depends(get_db),):
   
    error = None 
    if not username: 
        error = "Username is required."
    elif not password: 
        error = "Password is required."
    
    if error is None:
        user = schemas.UserCreate(
            name=username,
            password=generate_password_hash(password)
        )

        try: 
            crud.create_user(db, user)
        except sqlalchemy.exc.IntegrityError:
            error = "Username already in use."
        else: 
            return RedirectResponse(request.url_for('login'), status_code=303)
        
    flash(request, error)
    return RedirectResponse(request.url_for('register'), status_code=303)
    
    
@router.get('/login')
def login(request: Request):
    return TemplateResponse('auth/login.html', 
                            {'request': request})


@router.post('/login')
def login(request: Request,
          username: str | None = Form(None),
          password: str | None = Form(None),
          db: Session = Depends(get_db)):
    error = None
    if not username:
        error = "Username is required"
    elif not password: 
        error = "Password is required"
    
    if error is None: 
        user: schemas.User = schemas.User.from_orm(
            crud.get_user_from_name(db, username)
        )
        if not user: 
            error = "User does not exist."
            
        if not check_password_hash(user.password, password):
            error = "Incorrect password."
    
    if error is None:
        
        request.session['user'] = username
        
        return RedirectResponse(request.url_for('index'), status_code=303)
    
    else:
        flash(request, error)
        return RedirectResponse(
            request.url_for('login'), status_code=303
        )
    
    
    

@router.get('/logout')
def logout(request: Request):
    request.session.user = None
    
