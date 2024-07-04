from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User, Follow
from src.auth.schemas import UserIn


async def get_user_by_api_key(api_key: str, session: AsyncSession) -> User:
    stmt = select(User)\
        .filter(User.api_key == api_key)\
        .options(
            joinedload(User.user_followers).joinedload(Follow.follower), 
            joinedload(User.user_followings).joinedload(Follow.following)
        )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_api_with_followings(api_key: str, session: AsyncSession) -> User:
    stmt = select(User)\
        .filter(User.api_key == api_key)\
        .options(
            joinedload(User.user_followings).joinedload(Follow.following)
        )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_id(user_id: int, session: AsyncSession) -> User:
    stmt = select(User)\
        .filter(User.id == user_id)\
        .options(
            joinedload(User.user_followers).joinedload(Follow.follower), 
            joinedload(User.user_followings).joinedload(Follow.following)
        )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_id_with_followers(id: int, session: AsyncSession) -> User:
    stmt = select(User)\
        .filter(User.id == id)\
        .options(
            joinedload(User.user_followers).joinedload(Follow.follower)
        )
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_follow_by_following_id_and_follower_id(
        following_id: int, follower_id: int, session: AsyncSession
        ) -> Follow:
        stmt = select(Follow).filter(
            Follow.following_id == following_id,
            Follow.follower_id == follower_id
            )
        result = await session.execute(stmt)
        return result.scalars().first()



async def create_user(user_in: UserIn, api_key: str, session: AsyncSession) -> User:
    new_user = User(name=user_in.name, api_key=api_key)
    session.add(new_user)
    await session.commit()
    await get_user_by_api_key(api_key, session)
    return new_user


async def follow_user(user: User, following: User, session: AsyncSession) -> bool:
    if not user in following.followers and not following in user.followings:
        follow = Follow(following_id=following.id, follower_id=user.id)
        session.add(follow)
        await session.commit()
        return True
    return False


async def unfollow_user(user: User, following: User, session: AsyncSession) -> bool:
    if user in following.followers and following in user.followings:
        follow = await get_follow_by_following_id_and_follower_id(
            following_id=following.id, follower_id=user.id, session=session
            )      
        if follow:
            await session.delete(follow)
            await session.commit()
            return True
    return False