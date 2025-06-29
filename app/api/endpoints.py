from app.models.schemas import InputData, OutputData
from app.services.processor import process_data
from app.services.redis_service import get_all_by_key
from fastapi import APIRouter, Request

router = APIRouter()


@router.post('/process_data/', response_model=OutputData)
async def process(input_data: InputData, request: Request):
    """Обрабатывает входные данные и возвращает их вместе с фактом о кошках"""
    return await process_data(input_data)


@router.get('/history/')
async def get_history():
    """Возвращает всю историю запросов и ответов, сохранённую в Redis"""
    return await get_all_by_key('history')
