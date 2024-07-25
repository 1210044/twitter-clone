from typing import Dict
from fastapi import APIRouter, Header, HTTPException, Depends

from src.logger import logger
from src.db import get_session
from src.schemas import StatusResponse
from src.auth.schemas import UserIn, UserOut
from src.auth import service as UserService

router = APIRouter(prefix='/users')


@router.get('/me', response_model=UserOut)
async def get_user_me(api_key: str = Header(...), session = Depends(get_session)) -> Dict:
    user = await UserService.get_user_by_api_key(api_key, session)
    if not user:
        # raise HTTPException(status_code=404, detail="User not found")
        # Create user for test
        user_data = UserIn(name=api_key)
        user = await UserService.create_user(user_data, api_key, session)
    return {'user': user}


@router.get('/{user_id}', response_model=UserOut)
async def get_user_by_id(user_id: int, session = Depends(get_session)) -> Dict:
    user = await UserService.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {'user': user}


@router.post('', response_model=UserOut)
async def create_user(user_data: UserIn, api_key: str = Header(...), session = Depends(get_session)) -> Dict:
    user = await UserService.get_user_by_api_key(api_key, session)
    if user:
        return {'user': user}
    user = await UserService.create_user(user_data, api_key, session)
    return {'user': user}


@router.post('/{follow_id}/follow', response_model=StatusResponse)
async def follow_user_by_id(follow_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    user = await UserService.get_user_by_api_key(api_key, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    following = await UserService.get_user_by_id(follow_id, session)
    if not following:
        raise HTTPException(status_code=404, detail="User to follow not found")
    
    if user.id == following.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    await UserService.create_follow(user.id, follow_id, session)
    return StatusResponse()


@router.delete('/{follow_id}/follow', response_model=StatusResponse)
async def unfollow_user_by_id(follow_id: int, api_key: str = Header(...), session = Depends(get_session)) -> StatusResponse:
    user = await UserService.get_user_by_api_key(api_key, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    following = await UserService.get_user_by_id(follow_id, session)
    if following is None:
        raise HTTPException(status_code=404, detail="User to follow not found")
    
    if user.id == following.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")

    await UserService.delete_follow(user.id, follow_id, session)
    return StatusResponse()