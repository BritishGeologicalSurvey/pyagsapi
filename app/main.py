import logging
import os
from importlib import metadata
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
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from app.routes import validate, convert, ags_log, ags_export, ags_export_by_polygon
from app.routes.errors import HTTPExceptionResponse, InvalidPayloadError
from app.routes.utils import AGS_API_VERSION
from app.version import API_VERSION


def setup_logging(logging_level=logging.INFO):
    """Explicitly configure all loggers"""

    # Create console handler
    ch = logging.StreamHandler()
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)s%(reset)s | %(asctime)s | %(name)s | %(message)s"
    )
    ch.setFormatter(console_formatter)
    ch.setLevel(logging_level)

    # Configure request logger
    request_logger = logging.getLogger("request")
    request_logger.setLevel(logging_level)
    request_logger.handlers.clear()
    request_logger.addHandler(ch)
    request_logger.propagate = False

    # Configure uvicorn loggers
    logging.getLogger("uvicorn.access").handlers.clear()
    logging.getLogger("uvicorn.access").addHandler(ch)
    # INFO logs all requests including regular internal checks
    # which occur every few seconds. Turn down to WARNING
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").propagate = False

    logging.getLogger("uvicorn.error").handlers.clear()
    logging.getLogger("uvicorn.error").addHandler(ch)
    logging.getLogger("uvicorn.error").propagate = False

    # Configure app logger
    # Log application startup (these messages appear once for each uvicorn
    # worker as it starts).
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging_level)
    app_logger.addHandler(ch)
    app_logger.propagate = True

    # Start logging
    app_logger.info(
        f"Starting app instance: 'logging_level': {logging.getLevelName(logging_level)}"
    )


app = FastAPI(
    root_path=os.getenv("PYAGSAPI_ROOT_PATH", ""), docs_url=None, redoc_url=None
)

setup_logging()

# Add routes
app.include_router(validate.router)
app.include_router(convert.router)
app.include_router(ags_log.router)
app.include_router(ags_export.router)
app.include_router(ags_export_by_polygon.router)

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def landing_page(request: Request):
    return templates.TemplateResponse(
        "landing_page.html",
        {
            "request": request,
            "api_version_path": AGS_API_VERSION,
            "api_version": f'v{API_VERSION}',
            "agslib_version": f'v{metadata.version("python-ags4")}',
        },
    )


@app.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="AGS4 File Utilities Tool",
        swagger_favicon_url="//resources.bgs.ac.uk/webapps/resources/images/logos/cropped-BGS-favicon-logo-32x32.png",
    )


@app.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="AGS4 File Utilities Tool",
        redoc_favicon_url="//resources.bgs.ac.uk/webapps/resources/images/logos/cropped-BGS-favicon-logo-32x32.png",
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BGS AGS4 File Utilities Tool",
        summary="pyagsapi an API for validating, converting and exporting AGS files",
        version=API_VERSION,
        description=(
            "The API performs schema validation, data validation and conversion of your AGS files. "
            "It also exports a graphical log from AGS data held by NGDC. "
            "Schema validation and conversion uses https://gitlab.com/ags-data-format-wg/ags-python-library"
        ),
        terms_of_service="https://www.bgs.ac.uk/legal-and-policy/terms-of-use/",
        contact={
            "name": "BGS Enquiries",
            "url": "https://www.bgs.ac.uk/about-bgs/contact-us/",
            "email": "enquiries@bgs.ac.uk",
        },
        license_info={
            "name": "Open Government Licence v3",
            "url": "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/",
        },
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": (
            "https://raw.githubusercontent.com/BritishGeologicalSurvey/pyagsapi"
            "/main/app/static/img/BGS-Logo-Pos-RGB-01.png"
        )
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.client and not request.client.host.startswith("10."):
        logger = logging.getLogger("request")
        logger.info(f"called by {request.client.host}")
        req_id = shortuuid.ShortUUID().random(length=8)
        logger.info(f"Request: id: {req_id} path: {request.url}")
        logger.debug(f"Request: id: {req_id} headers: {request.headers}")
        start_time = time.time()

    response = await call_next(request)

    if request.client and not request.client.host.startswith("10."):
        call_time = int((time.time() - start_time) * 1000)
        logger.info(
            f"Request: id: {req_id} status: {response.status_code}, time: {call_time} ms"
        )
        logger.debug(f"Request: id: {req_id} response headers: {response.headers}")

    return response


# Override HTTPException
@app.exception_handler(StarletteHTTPException)
async def http_exception(request: Request, exc: StarletteHTTPException):
    error = HTTPExceptionResponse(request, exc)
    return JSONResponse(
        status_code=exc.status_code, content=jsonable_encoder(error.response())
    )


@app.exception_handler(InvalidPayloadError)
async def invalid_payload_exception(request: Request, exc: InvalidPayloadError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(exc.response()),
    )
