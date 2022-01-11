from requests import Response
from fastapi.testclient import TestClient
from fastapi import APIRouter, FastAPI


def test_factory(app, client): 
    
    @app.get('/test')
    def test():
        return {'message': 'hello'}
    
    r: Response = client.get('/test')  
    
    assert r.status_code == 200
    


