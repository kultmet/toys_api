from typing import Annotated

from fastapi import Depends, Request, routing
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.toys import crud, schemas, utils

toy_router = routing.APIRouter(prefix="/toys", tags=["Toys"])


@toy_router.get("", response_model=schemas.ToyPaginator)
async def featch_toys(
    request: Request,
    pagination: Annotated[schemas.Paginator, Depends(utils.paginate)],
    session: AsyncSession = Depends(get_async_session),
):
    result = await crud.featch_db_toys(session, page=pagination.page, size=pagination.size)
    result["next_page"] = utils.get_next_page_url(
        request, pagination.page, pagination.size, result.get("total_pages")
    )
    result["previous_page"] = utils.get_next_previous_url(
        request, pagination.page, pagination.size, result.get("total_pages")
    )
    return result
