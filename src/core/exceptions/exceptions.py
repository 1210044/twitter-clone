from fastapi import HTTPException


# === Auth Exceptions ===
class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(status_code=403, detail=detail)


# === User Exceptions ===
class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=404, detail=detail)

class UserToFollowNotFoundException(HTTPException):
    def __init__(self, detail: str = "User to follow not found"):
        super().__init__(status_code=404, detail=detail)

class FollowToYouSelfException(HTTPException):
    def __init__(self, detail: str = "You cannot follow yourself"):
        super().__init__(status_code=400, detail=detail)
