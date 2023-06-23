import logging

from fastapi import FastAPI

from Adapters.adapters import *
from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.ml_models.name_detection.level_1.heuristic import HeuristicModel
from Application.pdan import *
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title='MLSER')
logger = logging.getLogger("uvicorn.error")


@app.post('/check_project', response_model=ResponsePDF)
def single_pdf(id: int, extra_name: str, request_archive: UploadFile = File(...)):
    try:
        files_names = []
        list_fields = []

        files_pdf, header = ZipAdapter().parse(request_archive, id)

        for file_pdf in files_pdf:
            string_from_pdf = PDFAdapter().extract(header+'/'+file_pdf)
            list_fields.extend(HeuristicModel().execute(file_pdf, id, extra_name, string_from_pdf))
    except Exception as e:
        return ResponsePDF(
            id=1111,
            files=[]
        )
    return ResponsePDF(
            id=id,
            files=list_fields
    )