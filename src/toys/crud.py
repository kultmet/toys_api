import datetime
import math
from typing import List, Optional

from sqlalchemy import delete, desc, func, select, text, update
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query

from src.toys import models
from src.utils import SQLAlchemyRepository


async def featch_db_toys(session: AsyncSession, page, size):
    toy_repository = SQLAlchemyRepository(models.Toy, session)
    total_elements = await toy_repository.count()
    total_pages = total_pages = math.ceil(total_elements / size)
    content = await toy_repository.list(limit=size, offset=size * page)
    return {
        "content": content,
        "page": page,
        "size": size,
        "total_elements": total_elements,
        "total_pages": total_pages,
    }