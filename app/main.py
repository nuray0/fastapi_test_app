import httpx
import structlog
from app.api.endpoints import router
from app.core.exception_handlers import httpx_exception_handler
from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import LoggingMiddleware
from fastapi import FastAPI

setup_logging()
logger = structlog.get_logger()

app = FastAPI(title='Async FastAPI Data Processor')

app.add_middleware(LoggingMiddleware)
app.add_exception_handler(httpx.HTTPError, httpx_exception_handler)
app.include_router(router)
