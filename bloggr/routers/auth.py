from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from werkzeug.security import generate_password_hash, check_password_hash

from ..templates import TemplateResponse
from ..db import get_db, schemas, models

router = APIRouter(prefix='/auth')

@router.get('/register', response_class=HTMLResponse)
def register(request: Request):
    return TemplateResponse('auth/register.html', {'request': request})


@router.post('/register')
def register(request: Request,
             user: schemas.UserCreate = Depends(schemas.UserCreate),
             db: Session = Depends(get_db),):
    pass
    
    
    
    
@router.get('/login')
def login():
    pass

@router.post('/login')
def login():
    pass

@router.get('/logout')
def logout(request: Request):
    request.session.user = None
    
