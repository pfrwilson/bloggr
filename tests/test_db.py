
from bloggr.db import get_db, models, schemas, crud
from fastapi import Depends
from sqlalchemy.orm import Session, session
from sqlalchemy.exc import IntegrityError
import pytest
from pydantic import ValidationError

USER_CREATE = schemas.UserCreate(name='example', password='1234')
USER = schemas.User(name='example', password = '1234', id=1)


def test_get_db(app, client):
    
    @app.get('/test_db')
    def db_test(db: Session = Depends(get_db)):

        assert db is not None

        return {'message': 'success'}
    
    assert client.get('/test_db').status_code == 200

def add_user(db: Session = Depends(get_db)):    
    crud.create_user(db, USER_CREATE)
    return {'message': 'success'}

def get_user_by_id(id: int, db: Session = Depends(get_db)): 
    user: schemas.User = crud.get_user_from_id(db, id)
    return user
    
def get_user_by_name(name: str, db: Session = Depends(get_db)):
    user: schemas.User = crud.get_user_from_name(db, name)
    return user
    
def test_user_added(app, client):
    
    app.get('/add')(add_user)
    app.get('/get/')(get_user_by_id)
    app.get('/get-by-name/')(get_user_by_name)
    
    assert client.get('/add').status_code == 200
    
    assert schemas.User(**client.get('/get/?id=1').json()) == USER
    assert schemas.User(**client.get('/get-by-name/?name=example').json()) == USER    

def test_db_integrity(app, client):
    
    app.get('/add')(add_user)
    
    client.get('/add')

    with pytest.raises(IntegrityError):
        r = client.get('/add')
        #assert r.status_code == 404


def test_create_user_via_form(app, client):
    
    @app.post('/create/')
    def create_user(user: schemas.UserCreate = Depends(schemas.UserCreate),
                    db: Session = Depends(get_db)):
        
        crud.create_user(db, user)
        assert crud.get_user_from_name(db,'example') == USER
        assert crud.get_user_from_id(db, 1) == USER
          
    r = client.post('/create/', {'name': 'example', 'password': '1234'})
    assert r.status_code == 200    
    r = client.post('/create/', {'badform':'me'})
    assert r.status_code == 422
    
    
def test_user_does_not_exist(app, client):
    
    @app.get('/test')
    def test(db: Session = Depends(get_db)):
        
        assert get_user_by_name(db, 'Ralph') is None
        assert get_user_by_name(db, 10000) is None
        
    client.get('/')
        