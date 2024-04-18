import typing
from abc import ABC, abstractmethod

from sqlalchemy import Column, Insert, delete, func, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


def get_toy_data_from_exel():
    import numpy as np
    import pandas

    df = pandas.read_excel("files/detskiymir_msk_products.xlsx").replace(np.nan, None)
    return df.to_dict(orient="records")


def _get_field(model, key) -> Column:
    return model.__table__.c.get(key)


def _build_fields_for_request(model, field_names):
    return (_get_field(model, name) for name in field_names)


def build_column(column_or_name: typing.Union[Column, str], model=None):
    if isinstance(column_or_name, str):
        return _get_field(model, column_or_name)
    return column_or_name


class Criteries:
    def __init__(self, **criteries) -> None:
        self._criteries = criteries

    def add_model(self, model):
        self._model = model
        return self

    def _get_critery(self, model, key, value):
        return _get_field(model, key) == value

    def _build_equality_criteria(self, model, **kwargs):
        for key, value in kwargs.items():
            yield self._get_critery(model, key, value)

    def get_criteries(self):
        return self._build_equality_criteria(self._model, **self._criteries)


class Repository(ABC):
    @abstractmethod
    async def create(self, **data):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id):
        raise NotImplementedError

    @abstractmethod
    async def list(self, *creteries):
        raise NotImplementedError

    @abstractmethod
    async def update(self, *creteries, **data):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *creteries):
        raise NotImplementedError

    @abstractmethod
    async def one(self, *creteries):
        raise NotImplementedError


class SQLAlchemyRepository(Repository):
    def __init__(self, model, session: AsyncSession) -> None:
        self._model = model
        self._session: AsyncSession = session

    def _check_empty_criteries(self, criteries: typing.Optional[Criteries]) -> Criteries:
        if criteries is None:
            return Criteries()
        return criteries

    def _check_type(self, criteries):
        if not isinstance(criteries, (Criteries, type(None))):
            raise TypeError(
                "Required type 'Criteries' For "
                f"'criteries' argument, not '{type(criteries)}'"
            )
        return criteries

    def _add_returning_to_insert_or_update_stmt(
        self, stmt: Insert, columns: typing.Iterable, model
    ):
        if len(columns) > 0:
            columns = [build_column(column, model) for column in columns]
            return stmt.returning(*columns)
        return stmt

    async def _featch_one(self, stmt, columns: typing.Iterable):
        if len(columns) < 2:
            return (await self._session.execute(stmt)).scalar()
        return (await self._session.execute(stmt)).first()

    async def create(self, *columns, **data):
        stmt = insert(self._model).values(**data)
        stmt = self._add_returning_to_insert_or_update_stmt(stmt, columns, self._model)
        return await self._featch_one(stmt, columns)

    async def get(self, id):
        return await self._session.get(self._model, id)

    def _add_limit(self, stmt, limit=None):
        if limit:
            return stmt.limit(limit)
        return stmt

    def _add_offset(self, stmt, offset=None):
        if offset:
            return stmt.offset(offset)
        return stmt

    def _add_limit_and_offset(self, stmt, limit=None, offset=None):
        return self._add_offset(self._add_limit(stmt, limit), offset)

    def _get_list_stmt(self, model, columns, criteries):
        if not columns:
            return select(self._model).where(*criteries)
        columns = (build_column(column, model) for column in columns)
        return select(*columns).where(*criteries)

    async def _featch_all(self, stmt, columns: typing.Iterable):
        if len(columns) < 2:
            return (await self._session.execute(stmt)).scalars().all()
        return (await self._session.execute(stmt)).all()

    async def list(
        self,
        *columns: typing.Union[Column, str],
        criteries: typing.Optional[Criteries] = None,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
    ):
        self._check_type(criteries)
        criteries = (
            self._check_empty_criteries(criteries).add_model(self._model).get_criteries()
        )
        stmt = self._get_list_stmt(self._model, columns, criteries)
        stmt = self._add_limit_and_offset(stmt, limit, offset)
        return await self._featch_all(stmt, columns)

    async def update(self, *columns, criteries: typing.Optional[Criteries] = None, **data):
        self._check_type(criteries)
        criteries = (
            self._check_empty_criteries(criteries).add_model(self._model).get_criteries()
        )
        stmt = update(self._model).values(**data).where(*criteries)
        stmt = self._add_returning_to_insert_or_update_stmt(stmt, columns, self._model)
        return await self._featch_one(stmt, columns)

    async def one(self, *columns, criteries: typing.Optional[Criteries] = None):
        self._check_type(criteries)
        criteries = (
            self._check_empty_criteries(criteries).add_model(self._model).get_criteries()
        )
        stmt = self._get_list_stmt(self._model, columns, criteries)
        return await self._featch_one(stmt, columns)

    async def delete(self, criteries: typing.Optional[Criteries] = None):
        self._check_type(criteries)
        criteries = (
            self._check_empty_criteries(criteries).add_model(self._model).get_criteries()
        )
        return await self._session.execute(delete(self._model).where(*criteries))

    async def count(self, criteries: typing.Optional[Criteries] = None):
        return await self.one(func.count(self._model.id), criteries=criteries)
