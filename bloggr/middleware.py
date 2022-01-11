from fastapi import Request
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class FlashMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request.state.flash = request.session.pop('flash_cache', [])
        response = await call_next(request)
        return response

def get_flashed_messages(request: Request):
    messages = request.state.flash
    return messages

def flash(request: Request, message: str):
    messages = request.session.get('flash_cache', None)
    if not messages: 
        messages = []
    messages.append(message)
    request.session['flash_cache'] = messages



middleware = [
    Middleware(SessionMiddleware, secret_key = 'example'),
    Middleware(FlashMiddleware)
]

