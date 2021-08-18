import logging
import time

import colorlog
import shortuuid

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app import routes
from app.errors import HTTPExceptionResponse, InvalidPayloadError


def setup_logging(logging_level=logging.INFO):
    """Explicitly configure all loggers"""

    # Create console handler
    ch = logging.StreamHandler()
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s%(reset)s | %(asctime)s | %(name)s | %(message)s')
    ch.setFormatter(console_formatter)
    ch.setLevel(logging_level)

    # Configure request logger
    request_logger = logging.getLogger('request')
    request_logger.setLevel(logging_level)
    request_logger.handlers.clear()
    request_logger.addHandler(ch)
    request_logger.propagate = False

    # Configure uvicorn loggers
    logging.getLogger('uvicorn.access').handlers.clear()
    logging.getLogger('uvicorn.access').addHandler(ch)
    # INFO logs all requests including regular internal checks
    # which occur every few seconds. Turn down to WARNING
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').propagate = False

    logging.getLogger('uvicorn.error').handlers.clear()
    logging.getLogger('uvicorn.error').addHandler(ch)
    logging.getLogger('uvicorn.error').propagate = False

    # Log application startup (these messages appear once for each uvicorn
    # worker as it starts).
    app_logger = logging.getLogger(__name__)
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(ch)
    app_logger.propagate = False

    # Start logging
    app_logger.info(
        f"Starting app instance: "
        f"'logging_level': {logging.getLevelName(logging_level)}")


app = FastAPI()

setup_logging()

# Add routes
app.include_router(routes.router)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def homepage(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if not request.client.host.startswith('10.'):
        logger = logging.getLogger('request')
        logger.info(f"called by {request.client.host}")
        req_id = shortuuid.ShortUUID().random(length=8)
        logger.info(f"Request: id: {req_id} path: {request.url}")
        logger.debug(f"Request: id: {req_id} headers: {request.headers}")
        start_time = time.time()

    response = await call_next(request)

    if not request.client.host.startswith('10.'):
        call_time = int((time.time() - start_time) * 1000)
        logger.info(f"Request: id: {req_id} status: {response.status_code}, time: {call_time} ms")
        logger.debug(f"Request: id: {req_id} response headers: {response.headers}")

    return response


# Override HTTPException
@app.exception_handler(StarletteHTTPException)
async def http_exception(request: Request, exc: StarletteHTTPException):
    error = HTTPExceptionResponse(request, exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(error.response())
    )


@app.exception_handler(InvalidPayloadError)
async def invalid_payload_exception(request: Request, exc: InvalidPayloadError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(exc.response())
    )
