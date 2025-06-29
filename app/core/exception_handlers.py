import datetime

import httpx
import structlog
from fastapi import Request
from fastapi.responses import JSONResponse

logger = structlog.get_logger()


async def httpx_exception_handler(request: Request, exc: httpx.HTTPError):
    url = str(request.url)
    timestamp = datetime.datetime.now(datetime.UTC)
    exc_type = exc.__class__.__name__

    if isinstance(exc, httpx.HTTPStatusError):
        logger.error(
            'External API returned error status',
            url=url,
            error=str(exc),
            exception_type=exc_type,
            status_code=exc.response.status_code,
            timestamp=timestamp,
        )
        return JSONResponse(
            status_code=exc.response.status_code,
            content={'detail': 'External service returned an error.'},
        )

    elif isinstance(exc, httpx.ConnectError):
        logger.error(
            'External API connection error',
            url=url,
            error=str(exc),
            exception_type=exc_type,
            timestamp=timestamp,
        )
        return JSONResponse(
            status_code=502,
            content={'detail': 'Failed to connect to external service.'},
        )

    elif isinstance(exc, httpx.ConnectTimeout):
        logger.error(
            'External API connection timeout',
            url=url,
            error=str(exc),
            exception_type=exc_type,
            timestamp=timestamp,
        )
        return JSONResponse(
            status_code=504,
            content={'detail': 'External service connection timed out.'},
        )

    elif isinstance(exc, httpx.ReadTimeout):
        logger.error(
            'External API read timeout',
            url=url,
            error=str(exc),
            exception_type=exc_type,
            timestamp=timestamp,
        )
        return JSONResponse(
            status_code=504,
            content={'detail': 'Timeout while reading from external service.'},
        )

    else:
        logger.error(
            'Unhandled HTTPX error',
            url=url,
            error=str(exc),
            exception_type=exc_type,
            timestamp=timestamp,
        )
        return JSONResponse(
            status_code=502,
            content={'detail': 'Error communicating with external service.'},
        )
