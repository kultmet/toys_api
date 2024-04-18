from fastapi import Query, Request

from src.toys import schemas


def paginate(
    page: int = Query(ge=0, default=0), size: int = Query(ge=1, le=50, default=10)
):
    return schemas.Paginator(page=page, size=size)


def get_next_page_url(request: Request, page, size, total_pages):
    """Получить следующую страницу. Для пагинатора

    Args:
        request (Request): Обьект Request
        page (int): Номер страници
        size (int): Размер страници
        total_pages (int): всего страниц

    Returns:
        str: URL string
    """
    if not total_pages:
        return None
    if page > total_pages:
        return None
    return request.url.replace_query_params(page=page + 1, size=size).__str__()


def get_next_previous_url(request: Request, page, size, total_pages):
    """Получить предидущую страницу. Для пагинатора

    Args:
        request (Request): Обьект Request
        page (int): Номер страници
        size (int): Размер страници
        total_pages (int): всего страниц

    Returns:
        str: URL string
    """
    if not total_pages:
        return None
    if page == 0:
        return None
    return request.url.replace_query_params(page=page - 1, size=size).__str__()
