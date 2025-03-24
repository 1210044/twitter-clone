# from sqlalchemy import select, insert, delete
# from sqlalchemy.orm import joinedload
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.auth.models import User, Follow
# from src.auth.schemas import UserIn


# async def get_user_by_api_key(api_key: str, session: AsyncSession) -> User:
#     stmt = (
#         select(User)
#         .filter(User.api_key == api_key)
#         .options(
#             joinedload(User.user_followers).joinedload(Follow.follower),
#             joinedload(User.user_followings).joinedload(Follow.following),
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
