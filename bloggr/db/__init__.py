from fastapi.applications import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.util.langhelpers import _update_argspec_defaults_into_env
from starlette.requests import Request, empty_receive

from .models import metadata

#DATABASE_URL = "sqlite:///./sql_app.db" 
#
#engine = create_engine(
#    DATABASE_URL, connect_args={"check_same_thread": False}
#)
#
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(app: FastAPI):
    
    assert hasattr(app.state, 'database_url'), 'no url specified'
    
    engine = create_engine(
        app.state.database_url
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    metadata.bind = engine
    metadata.create_all()
    
    app.state.db = {
        "session": SessionLocal, 
        "metadata": metadata, 
        "engine": engine
    }

def get_db(request: Request) -> Session:
    
    app = request.app
    assert hasattr(app.state, 'db')
    db = app.state.db['session']()
    try:
        yield db
    finally:
        db.close()



