from typing import Optional, List

from pydantic import BaseModel
from fastapi import UploadFile


class InputSinglePDF(BaseModel):
    id: int
    extra_name: str


class Files(BaseModel):
    file_name: str
    folder: str
    name: str
    description: Optional[str]
    page: int


class ResponsePDF(BaseModel):
    id: int
    files: List[Files]