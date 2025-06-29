from datetime import datetime, timezone

import httpx
import structlog
from app.utils.logging_utils import trim_body

logger = structlog.get_logger()


async def fetch_cat_fact() -> str:
    url = 'https://catfact.ninja/fact'
    logger.info(
        'Sending request to external API',
        url=str(url),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

    async with httpx.AsyncClient() as client:
        r = await client.get(url, timeout=5.0)
        r.raise_for_status()
        fact = r.json().get('fact', 'No fact found')
        return fact
