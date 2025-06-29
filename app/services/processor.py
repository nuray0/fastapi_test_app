import structlog
from app.models.schemas import InputData, OutputData
from app.services.cat_api import fetch_cat_fact
from app.services.redis_service import save_request_response

logger = structlog.get_logger()


async def process_data(data: InputData) -> OutputData:
    cat_fact = await fetch_cat_fact()

    response = OutputData(received_data=data.payload, cat_fact=cat_fact)

    await save_request_response(
        'history', {'input': data.payload, 'output': response.model_dump()}
    )

    return response
