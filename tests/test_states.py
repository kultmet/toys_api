import pytest
from sqlalchemy import delete, engine, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import BinaryExpression

from src.toys import models, schemas
from src.utils import Criteries, SQLAlchemyRepository, build_column
from tests.conftest import async_session_maker

TestModel = models.Toy


class TestStates:
    def test_create_criteries_object(self):
        criteries = Criteries(id=1, name="тестовая")
        assert criteries._criteries == {"id": 1, "name": "тестовая"}
        with pytest.raises(AttributeError) as e:
            criteries._model
            criteries.get_criteries()
        criteries.add_model(TestModel)
        assert criteries._model == TestModel
        creteries_result = criteries.get_criteries()
        id_cretery = creteries_result.__next__()
        toy_name_cretery = creteries_result.__next__()
        assert isinstance(id_cretery, BinaryExpression)
        assert id_cretery.__str__() == (TestModel.id == 1).__str__()
        assert toy_name_cretery.__str__() == (models.Toy.name == "тестовая").__str__()
        creteries_result = criteries.get_criteries()
        result = [*creteries_result]
        assert len(result) == 2

    def test_create_empty_criteries_object(self):
        empty_criteries = Criteries()
        empty_criteries.add_model(models.Toy)
        creteries_result = empty_criteries.get_criteries()
        result = [*creteries_result]
        assert len(result) == 0

    @pytest.mark.asyncio
    async def test_sqllalchemy_migrations_and_repository_list(self):
        session: AsyncSession = None
        async with async_session_maker() as session:
            db_toy = (await session.execute(select(TestModel))).scalars().all()
            assert len(db_toy) == 41147
            repository = SQLAlchemyRepository(TestModel, session=session)
            with pytest.raises(TypeError):
                await repository.list(criteries=1)
            name = "Конструктор SLUBAN Сапфировый замок"
            db_result = await repository.list(criteries=Criteries(name=name))
            len(db_result)
            assert len(db_result) == 1
