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


class ConfigurationIMGParser(BaseModel):
    name_model: Optional[str]
    level_using: int #[0-not uses, 1-use only for img page, 2-use always]


class Configuration(BaseModel):
    config_model: ConfigurationIMGParser = ConfigurationIMGParser(level_using=0)
    level_detection: int = 0
