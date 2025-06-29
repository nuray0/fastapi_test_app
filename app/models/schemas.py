from typing import Any, Dict

from pydantic import BaseModel


class InputData(BaseModel):
    payload: Dict[str, Any]


class OutputData(BaseModel):
    received_data: Dict[str, Any]
    cat_fact: str
