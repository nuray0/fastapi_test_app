import datetime

import structlog
from app.utils.logging_utils import loggable_trimmed_response, trim_body
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        method = request.method
        url = str(request.url)

        try:
            body_bytes = await request.body()
            body_str = body_bytes.decode(errors='ignore')
            logger.info(
                f'Request | method={method} | url={url} | body={trim_body(body_str)}',
                timestamp=datetime.datetime.now(datetime.UTC),
            )
        except Exception as e:
            logger.warning('Could not read request body', error=str(e))

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                'Exception during request processing',
                url=url,
                error=str(e),
                timestamp=datetime.datetime.now(datetime.UTC),
            )
            return JSONResponse(
                status_code=500,
                content={'detail': 'Internal Server Error'},
            )

        try:
            response_body = b''
            async for chunk in response.body_iterator:
                response_body += chunk
            response.body_iterator = iter([response_body])

            response_text = response_body.decode(errors='ignore')
            trimmed_response_text = loggable_trimmed_response(response_text)

            logger.info(
                f'Response | method={method} | url={url} | status={response.status_code} | {trimmed_response_text}',
                timestamp=datetime.datetime.now(datetime.UTC),
            )

            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        except Exception as e:
            logger.warning('Could not read response body', error=str(e))
            return response
