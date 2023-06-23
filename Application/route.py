import logging

from fastapi import FastAPI

from Adapters.adapters import *
from Application.application import ExecuteModel
from Application.pdan import *
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title='MLSER')
logger = logging.getLogger("uvicorn.error")


@app.post('/check_project', response_model=ResponsePDF)
def single_pdf(id: int, extra_name: str, request_archive: UploadFile = File(...)):
    try:
        files_names = []
        list_fiels = []

        # id, extra_name, archive = JSONAdapter().parse(request, request_archive)

        files_pdf = ZipAdapter().parse(request_archive, id)

        for file_pdf in files_pdf:
            pages_in_pdf = PDFAdapter().extract(file_pdf)
            for num_page, page_text in enumerate(pages_in_pdf):
                list_fiels.extend(ExecuteModel().execute(file_pdf, num_page, id, extra_name))
    except Exception as e:
        return ResponsePDF(
            id=1111,
            files=[]
        )
    return ResponsePDF(
            id=id,
            files=list_fiels
    )