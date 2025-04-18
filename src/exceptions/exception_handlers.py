from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from src.schemas.error_schema import ErrorBase, ErrorOut, ValidationErrors


async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorOut(
            result=False, error_type=type(exc).__name__, error_message=exc.detail
        ).__dict__,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    response_errors = []
    for error in exc.errors():
        response_errors.append(
            ErrorBase(error_type=error["type"], error_message=error["msg"])
        )
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            ValidationErrors(result=False, errors=response_errors)
        ),
    )
