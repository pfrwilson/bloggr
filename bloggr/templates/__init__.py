
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(directory=os.path.dirname(__file__))

TemplateResponse = templates.TemplateResponse

