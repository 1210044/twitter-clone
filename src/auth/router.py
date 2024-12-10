from typing import Dict
from fastapi import APIRouter, Header, Depends

from src.db import get_session
from src.schemas import StatusResponseTrue, ErrorResponse
from src.auth.schemas import UserIn, UserOut
from src.auth import exceptions, crud as UserCrud


router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/me', response_model=UserOut, responses={404: {"model": ErrorResponse}})
async def get_user_me(api_key: str = Header(...), session = Depends(get_session)) -> Dict:
    user_data = UserIn(name=api_key)
    user = await UserCrud.create_user(user_data, api_key, session)
    return {'user': user}


@router.get('/{user_id}', response_model=UserOut, responses={404: {"model": ErrorResponse}})
async def get_user_by_id(user_id: int, session = Depends(get_session)) -> Dict:
    user = await UserCrud.get_user_by_id(user_id, session)
    if not user:
        raise exceptions.UserNotFoundException()
    return {'user': user}


@router.post('', response_model=UserOut)
async def create_user(user_data: UserIn, api_key: str = Header(...), session = Depends(get_session)) -> Dict:
    user = await UserCrud.create_user(user_data, api_key, session)
    return {'user': user}


@router.post('/{follow_id}/follow', response_model=StatusResponseTrue, responses={404: {"model": ErrorResponse}})
async def follow_user_by_id(follow_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponseTrue:
    user = await UserCrud.get_user_by_api_key(api_key, session)
    if not user:
        raise exceptions.UserNotFoundException()
    
    following = await UserCrud.get_user_by_id(follow_id, session)
    if not following:
        raise exceptions.UserToFollowNotFoundException()
    
    if user.id == following.id:
        raise exceptions.FollowToYouSelfException()

    await UserCrud.create_follow(user.id, follow_id, session)
    return StatusResponseTrue()


@router.delete('/{follow_id}/follow', response_model=StatusResponseTrue, responses={404: {"model": ErrorResponse}})
async def unfollow_user_by_id(follow_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponseTrue:
    user = await UserCrud.get_user_by_api_key(api_key, session)
    if user is None:
        raise exceptions.UserNotFoundException()

    following = await UserCrud.get_user_by_id(follow_id, session)
    if following is None:
        raise exceptions.UserToFollowNotFoundException()
    
    if user.id == following.id:
        raise exceptions.FollowToYouSelfException()

    await UserCrud.delete_follow(user.id, follow_id, session)
    return StatusResponseTrue()