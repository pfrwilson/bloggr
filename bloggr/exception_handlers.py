from fastapi import responses
from fastapi.exceptions import RequestValidationError
from fastapi import Request, status
from .middleware import flash
from fastapi.responses import RedirectResponse, JSONResponse
from urllib.parse import urljoin
from fastapi.encoders import jsonable_encoder

def flash_validation_errors(request: Request, exc: RequestValidationError):
    
    if request.method == 'post':
    
        def parse_single_error(error: dict):
            msg = error['msg']
            field = error['loc'][1]
            type = error['type']
            return {'msg': msg, 'field': field, 'type': type}
            
        for error in exc.errors():
            flash(request, parse_single_error(error))
        
        return RedirectResponse(
            request.url,
        )
    
    else:
        return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )