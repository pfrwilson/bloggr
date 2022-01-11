
import fastapi
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_307_TEMPORARY_REDIRECT
from bloggr.exception_handlers import flash_validation_errors
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bloggr.middleware import flash, get_flashed_messages
from uvicorn import run

def test_flash_handler(app, client):
    
    @app.exception_handler(RequestValidationError)
    def flash(*args, **kwargs):
        return flash_validation_errors(*args, **kwargs)
    
    #@app.exception_handler(RequestValidationError)
    #async def validation_exception_handler(request: Request, exc: RequestValidationError):
    #    return JSONResponse(
    #        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    #    )
    #
    @app.get('/')
    def get(number: int, word: str):
        pass
    
    @app.post('/test_post')
    def post(number: int, word: str):
        pass

    @app.get('/test_post')
    def test_get(number:int, word: str):
        pass
    
    @app.get('/flashes')
    def get_flashed(request: Request):
        return {'messages': get_flashed_messages(request)}
        
    r = client.get('/?number=hello&str=word')
    assert r.status_code == 422
    
    r = client.post('/test_post/?number=hello&word=str')
    assert r.status_code == status.HTTP_307_TEMPORARY_REDIRECT
    
    r = client.get('/flashes')
    assert r.json() is None
    