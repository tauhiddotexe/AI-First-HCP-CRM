from pydantic import BaseModel


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = 'Operation successful'
    data: dict | list | None = None


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    message: str = 'Operation failed'
    errors: list[ErrorDetail] | None = None


class PaginatedResponse(BaseModel):
    items: list
    page: int
    limit: int
    total: int
    pages: int
