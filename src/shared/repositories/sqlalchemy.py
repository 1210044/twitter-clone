from typing import Any, List, Type, TypeVar, Optional, Generic
from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Load, load_only, defer
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SqlAlchemyRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self._session_factory = db_session
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        async with self._session_factory() as session:
            instance = self.model(**data.model_dump())
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        async with self._session_factory() as session:
            stmt = update(self.model).values(**data.model_dump(exclude_unset=True)).filter_by(**filters).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> None:
        async with self._session_factory() as session:
            await session.execute(delete(self.model).filter_by(**filters))
            await session.commit()

    async def get_single(
        self,
        *options: Load,
        fields: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
        **filters
    ) -> Optional[ModelType]:
        async with self._session_factory() as session:
            stmt = select(self.model).filter_by(**filters)
            field_options = []
            
            if fields:
                model_fields = [getattr(self.model, field) for field in fields]
                field_options.append(load_only(*model_fields))
            
            if exclude:
                excluded_fields = [getattr(self.model, field) for field in exclude]
                field_options.append(defer(*excluded_fields))
            
            all_options = list(options) + field_options
            
            if all_options:
                stmt = stmt.options(*all_options)
            
            row = await session.execute(stmt)
            return row.scalar_one_or_none()

    async def get_multi(
            self,
            order: str = "id",
            limit: int = 100,
            offset: int = 0
    ) -> List[ModelType]:
        async with self._session_factory() as session:
            order_clause = getattr(self.model, order)
            stmt = select(self.model).order_by(order_clause).limit(limit).offset(offset)
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
                for key, value in filters.items():
                    field = getattr(self.model, key)
                    if isinstance(value, list):
                        stmt = stmt.where(field.in_(value))
                    else:
                        stmt = stmt.where(field == value)

            if order:
                order_clauses = []
                for order_field in order:
                    if order_field.startswith('-'):
                        order_clauses.append(getattr(self.model, order_field[1:]).desc())
                    else:
                        order_clauses.append(getattr(self.model, order_field).asc())
                stmt = stmt.order_by(*order_clauses)

            if limit is not None:
                stmt = stmt.limit(limit)
            if offset is not None:
                stmt = stmt.offset(offset)

            row = await session.execute(stmt)
            return row.scalars().all()

    async def all(self) -> List[ModelType]:
        return await self.filter()

    async def exists(self, **filters) -> bool:
        stmt = select(self.model).filter_by(**filters)
        async with self._session_factory() as session:
            result = await session.execute(stmt)
            return result.scalar() is not None