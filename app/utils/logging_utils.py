import json


def trim_body(text: str, max_length: int = 100) -> str:
    """Обрезает строку до указанной длины - 100, добавляя '...', если строка длиннее"""
    return text if len(text) <= max_length else text[:max_length] + '...'


def loggable_trimmed_response(response_text: str) -> str:
    """Извлекает и сокращает поля 'received_data' и 'cat_fact' при наличии"""
    try:
        response_json = json.loads(response_text)
        trimmed_parts = []

        if 'received_data' in response_json:
            trimmed = trim_body(json.dumps(response_json['received_data']))
            trimmed_parts.append(f'received_data={trimmed}')

        if 'cat_fact' in response_json:
            trimmed = trim_body(str(response_json['cat_fact']))
            trimmed_parts.append(f'cat_fact={trimmed}')

        if not trimmed_parts:
            trimmed_parts.append(f'body={trim_body(response_text)}')

        return ' | '.join(trimmed_parts)

    except Exception:
        return f'body={trim_body(response_text)}'
