import enum
import json
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, HttpUrl
from sqlalchemy import desc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncConnection


class ToyResponse(BaseModel):
    name: str
    articul: str
    gost: Optional[str]
    brand: str
    category: str
    nomenclature: str
    category_path: str
    price: int
    url: str
    warehouse: Optional[str]
    count: Optional[int]
    instock: Optional[int]
    city: str
    updated_at: Optional[datetime]
    discount_price: Optional[float]
    razmer: Optional[str]


class Paginator(BaseModel):
    page: int
    size: int
    total_elements: Optional[int] = None
    total_pages: Optional[int] = None
    next_page: Optional[HttpUrl] = None
    previous_page: Optional[HttpUrl] = None


class ToyPaginator(Paginator, BaseModel):
    content: List[ToyResponse]
