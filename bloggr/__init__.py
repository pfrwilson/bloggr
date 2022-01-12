from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .middleware import middleware
from .routers import auth, blog
from .db import init_db
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATABASE_URL = "sqlite:///./sql_app.db" 

def get_app(config: dict | None = None):
    
    app = FastAPI(middleware = middleware)
    
    url = DEFAULT_DATABASE_URL
    if config: 
        url = config.get('database_url', DEFAULT_DATABASE_URL)
    app.state.database_url = url
    init_db(app)
    
    app.mount('/static', StaticFiles(directory=os.path.join(APP_DIR, 'static')), name='static')

    app.include_router(auth.router)
    app.include_router(blog.router)
    
    return app


app = get_app()

