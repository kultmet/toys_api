from typing import Annotated

from fastapi import Depends, Request, routing
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.toys import crud, schemas, utils

toy_router = routing.APIRouter(prefix="/toys", tags=["Toys"])


@toy_router.get("/ex")
def read_xlsx():
    toy_types = {}
    import numpy as np
    import pandas

    df = pandas.read_excel("files/detskiymir_msk_products.xlsx").replace(np.nan, None)
    toys_data = df.to_dict(orient="records")
    for toy in toys_data:
        for k, v in toy.items():
            if k not in toy_types:
                toy_types[k] = set()
            toy_types[k].add(type(v).__name__)
    # print()
    import json

    print(json.dumps(toy_types, indent=2, default=str))
    return toys_data[:10]


@toy_router.get(
    "", response_model=schemas.ToyPaginator
)  # , response_model=schemas.ToyPaginator
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
