import json
import time
import requests
from fastapi import UploadFile, File
from pydantic import BaseModel
from typing import Optional

from Application.pdan import Configuration, ConfigurationIMGParser, ConfigurationValidator

extra_name = 'Общество с ограниченной ответственностью "КАББАЛКГИПРОТРАНС"'
config = Configuration(
    img_model=ConfigurationIMGParser(name_model='tesseract', level_using=0),
    validator_model=ConfigurationValidator(name_model='default'),
    level_detection=0
)
file_path = 'D:/12.zip'
request_archive = UploadFile(file_path)

url = 'http://178.205.138.31:6432/check_project_advance'

# Prepare the request data
data = {
    'id': 12,
    'extra_name': extra_name,
}

# Create the files dictionary
files = {
    'request_archive': request_archive.file,
    'config': json.dumps(config.dict()).encode('utf-8')
}

start_time = time.time()
response = requests.post(url, params=data, files=files)
end_time = time.time()
request_time = end_time - start_time
print(f"Время выполнения запроса: {request_time} секунд")
print(response.json())