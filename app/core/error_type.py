from fastapi import HTTPException, status

class BaseError(HTTPException):
  def __init__(self, status_code: int, detail: str):
    super().__init__(status_code=status_code, detail=detail)

class BadRequestError(BaseError):
  def __init__(self, detail: str = "Solicitud incorrecta"):
    super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedError(BaseError):
  def __init__(self, detail: str = "No autorizado"):
    super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

class ForbiddenError(BaseError):
  def __init__(self, detail: str = "Acceso prohibido"):
    super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

class ResourceNotFoundError(BaseError):
  def __init__(self, detail: str = "Recurso no encontrado"):
    super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class DuplicateResourceError(BaseError):
  def __init__(self, detail: str = "Recurso duplicado"):
    super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
