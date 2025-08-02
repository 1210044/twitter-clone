from typing import Dict, List, Optional, Any
from sqlalchemy.orm import selectinload
from enum import StrEnum

from src.shared.repositories.sqlalchemy import SqlAlchemyRepository
from src.core.config.database.db_helper import db_helper
from src.modules.users.models import User
from src.modules.users.models import Follow
from src.modules.users.schemas import UserCreate, UserUpdate


class UserLoadOption(StrEnum):
    FOLLOWERS = "followers"
    FOLLOWING = "following"


class UserRepository(SqlAlchemyRepository[User, UserCreate, UserUpdate]):
    _LOAD_OPTIONS = {
        UserLoadOption.FOLLOWERS: selectinload(User.user_followers).selectinload(Follow.follower),
        UserLoadOption.FOLLOWING: selectinload(User.user_followings).selectinload(Follow.following),
    }
    
    async def get_user(
        self,
        *,
        filters: Optional[Dict[str, Any]] = None,
        load_options: Optional[List[UserLoadOption]] = None,
    ) -> Optional[User]:
        options_list = []
        
        # Применяем выбранные стратегии загрузки
        if load_options:
            for option in load_options:
                strategy = self._LOAD_STRATEGIES.get(option)
                
                if isinstance(strategy, list):
                    options_list.extend(strategy)
                elif strategy:
                    options_list.append(strategy)
        
        return await self.get_one(*options_list, **(filters or {}))


user_repository = UserRepository(model=User, db_session=db_helper.get_db_session)


# from sqlalchemy import select, insert, delete
# from sqlalchemy.orm import joinedload, se
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.auth.models import User, Follow
# from src.auth.schemas import UserIn


# async def get_user_by_api_key(api_key: str, session: AsyncSession) -> User:
#     stmt = (
#         select(User)
#         .filter(User.api_key == api_key)
#         .options(
#             selectinload(User.user_followers).selectinload(Follow.follower),
#             selectinload(User.user_followings).selectinload(Follow.following),
#         )
#     )
#     result = await session.execute(stmt)
#     return result.scalars().first()


# async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
#     stmt = (
#         select(User)
#         .filter(User.id == user_id)
#         .options(
#             joinedload(User.user_followers).joinedload(Follow.follower),
#             joinedload(User.user_followings).joinedload(Follow.following),
#         )
#     )
#     result = await session.execute(stmt)
#     return result.scalars().first()


# async def create_user(user_in: UserIn, api_key: str, session: AsyncSession) -> User:
#     user = await get_user_by_api_key(api_key, session)
#     if not user:
#         stmt = insert(User).values(
#             api_key=api_key,
#             name=user_in.name,
#         )
#         await session.execute(stmt)
#         await session.commit()
#         user = await get_user_by_api_key(api_key, session)
#     return user


# async def get_follow_by_following_id_and_follower_id(
#     following_id: int, follower_id: int, session: AsyncSession
# ) -> Follow:
#     stmt = select(Follow).filter(
#         Follow.following_id == following_id, Follow.follower_id == follower_id
#     )
#     result = await session.execute(stmt)
#     return result.scalar_one_or_none()


# async def create_follow(user_id: int, follow_id: User, session: AsyncSession) -> None:
#     follow = await get_follow_by_following_id_and_follower_id(
#         following_id=follow_id, follower_id=user_id, session=session
#     )
#     if not follow:
#         stmt = insert(Follow).values(following_id=follow_id, follower_id=user_id)
#         await session.execute(stmt)
#         await session.commit()


# async def delete_follow(user_id: int, follow_id: int, session: AsyncSession) -> None:
#     follow = await get_follow_by_following_id_and_follower_id(
#         following_id=follow_id, follower_id=user_id, session=session
#     )
#     if follow:
#         stmt = delete(Follow).where(
#             Follow.following_id == follow_id, Follow.follower_id == user_id
#         )
#         await session.execute(stmt)
#         await session.commit()
