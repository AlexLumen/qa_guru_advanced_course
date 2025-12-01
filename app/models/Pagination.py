from pydantic import BaseModel


class Pagination(BaseModel):
    page: int
    size: int
    items: list
    total: int
    pages: int
