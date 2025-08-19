from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.error_type import BaseError

def setup_exception_handlers(app: FastAPI) -> None:
    """
    Configura todos los exception handlers para la aplicación FastAPI
    """
    
    @app.exception_handler(BaseError)
    async def base_error_handler(request: Request, exc: BaseError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail,
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": "error",
                "message": exc.detail,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # Convierte los errores de validación a tu formato
        errors = [
            {"field": ".".join(str(loc) for loc in err["loc"][1:]), "message": err["msg"]} 
            for err in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            content={
                "status": "error",
                "message": "Error de validación",
                "errors": errors,
            },
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # Maneja errores 500 inesperados
        print(f"Error interno: {exc}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Error interno del servidor",
            },
        )