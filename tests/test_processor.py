from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest
from app.main import app
from fastapi import status
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_process_data_success():
    payload = {'payload': {'hello': 'world'}}
    expected_fact = 'Cats sleep 16 hours a day'

    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json = lambda: {'fact': expected_fact}
    mock_response.raise_for_status = Mock()

    with patch(
        'app.services.cat_api.httpx.AsyncClient.get',
        return_value=mock_response,
    ), patch(
        'app.services.processor.save_request_response', new_callable=AsyncMock
    ):

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url='http://test'
        ) as ac:
            response = await ac.post('/process_data/', json=payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['cat_fact'] == expected_fact


@pytest.mark.asyncio
async def test_process_data_httpx_error():
    payload = {'payload': {'hello': 'world'}}

    with patch(
        'app.services.cat_api.httpx.AsyncClient.get',
        side_effect=httpx.HTTPError('External API error'),
    ), patch(
        'app.services.processor.save_request_response', new_callable=AsyncMock
    ):

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url='http://test'
        ) as ac:
            response = await ac.post('/process_data/', json=payload)

        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert response.json() == {
            'detail': 'Error communicating with external service.'
        }


@pytest.mark.asyncio
async def test_process_data_unhandled_exception():
    payload = {'payload': {'hello': 'world'}}

    with patch(
        'app.services.processor.fetch_cat_fact',
        side_effect=Exception('Unhandled exception'),
    ), patch(
        'app.services.processor.save_request_response', new_callable=AsyncMock
    ):

        transport = ASGITransport(app=app)
        async with AsyncClient(
            transport=transport, base_url='http://test'
        ) as ac:
            response = await ac.post('/process_data/', json=payload)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {'detail': 'Internal Server Error'}
