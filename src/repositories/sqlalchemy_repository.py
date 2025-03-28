from typing import Any, List, Type, TypeVar, Optional, Generic

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.orm import load_only, selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base_model import Base

from .base_repository import AbstractRepository


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SqlAlchemyRepository(AbstractRepository, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self._session_factory = db_session
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        async with self._session_factory() as session:
            instance = self.model(**data)
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        async with self._session_factory() as session:
            stmt = update(self.model).values(**data).filter_by(**filters).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> None:
        async with self._session_factory() as session:
            await session.execute(delete(self.model).filter_by(**filters))
            await session.commit()

    async def get_single(self, **filters) -> Optional[ModelType] | None:
        async with self._session_factory() as session:
            row = await session.execute(select(self.model).filter_by(**filters))
            return row.scalar_one_or_none()
    
    async def get_single(
        self, 
        related: Optional[List[str]] = None, 
        join_related: Optional[List[str]] = None, 
        **filters
    ) -> Optional[ModelType]:
        async with self._session_factory() as session:
            stmt = select(self.model).filter_by(**filters)

            if related:
                stmt = stmt.options(*(selectinload(getattr(self.model, relation)) for relation in related))

            if join_related:
                stmt = stmt.options(*(joinedload(getattr(self.model, relation)) for relation in join_related))

            row = await session.execute(stmt)
            return row.scalar_one_or_none()

    async def get_multi(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0
    ) -> List[ModelType]:
        async with self._session_factory() as session:
            stmt = select(self.model).order_by(*order).limit(limit).offset(offset)
            row = await session.execute(stmt)
            return row.scalars().all()

    async def filter(
            self,
            filters: dict[str, Any] | None = None,
            fields: list[str] | None = None,
            order: list[str] | None = None,
            limit: int = 100,
            offset: int = 0,
    ) -> List[ModelType] | None:
        async with self._session_factory() as session:
            stmt = select(self.model)

            if fields:
                model_fields = [getattr(self.model, field) for field in fields]
                stmt = stmt.options(load_only(*model_fields))

            if filters:
                conditions = []
                for key, value in filters.items():
                    field = getattr(self.model, key)
                    if isinstance(value, list):
                        conditions.append(field.in_(value))
                    else:
                        conditions.append(field == value)
                stmt = stmt.where(*conditions)

            if order:
                stmt = stmt.order_by(*order)
            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)

            row = await session.execute(stmt)
            return row.scalars().all()

    async def all(self) -> List[ModelType] | None:
        return await self.filter()

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None