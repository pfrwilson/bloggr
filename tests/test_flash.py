
from fastapi import Request, requests
from starlette.responses import Response
from bloggr.middleware import FlashMiddleware, flash, get_flashed_messages
from fastapi import FastAPI
from pytest import MonkeyPatch

def trigger_flash(request: Request):
    
    flash(request, 'message_1')
    flash(request, 'message_2')
    
    assert isinstance(request.session, dict)
    assert request.session['flash_cache'] == ['message_1', 'message_2']
    
    return {'message': 'success'}
    

def get_flashed(request: Request):
    
    return {'messages': get_flashed_messages(request)}

    
def test_flashes(app: FastAPI, client, monkeypatch):

    app.get('/trigger_flash')(trigger_flash)
    app.get('/get_flashed')(get_flashed)
    
    r = client.get('/trigger_flash')
    
    assert r.status_code == 200
    
    r = client.get('/get_flashed')
    
    assert r.json()['messages'] == ['message_1', 'message_2']
    
    r = client.get('/get_flashed')
    
    assert r.json()['messages'] == []