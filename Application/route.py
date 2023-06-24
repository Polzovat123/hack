import logging
from concurrent.futures import ProcessPoolExecutor

import requests
from fastapi import FastAPI
import shutil
import fasttext.util

from Adapters.adapters import *
from Application.dialog import dialog_paradigm
from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.ml_models.name_detection.level_1.heuristic import HeuristicModel
from Application.ml_models.name_detection.level_2.fasttext_model import FastTextModel
from Application.ml_models.name_detection.level_3.sbert import SBERTModel
from Application.pdan import *
from fastapi import FastAPI, UploadFile, File

app = FastAPI(title='MLSER')
logger = logging.getLogger("uvicorn.error")
fasttext.util.download_model('ru')


def process_file(file_pdf, id, extra_name, string_from_pdf, level_naming_detection=1, session=False):
    files = []
    if level_naming_detection == 1:
        files = HeuristicModel().execute(file_pdf, id, extra_name, string_from_pdf)
    elif level_naming_detection == 2:
        files = FastTextModel().execute(file_pdf, id, extra_name, string_from_pdf)
    elif level_naming_detection == 3:
        files = SBERTModel().execute(file_pdf, id, extra_name, string_from_pdf)
    else:
        files = ExecuteModel.execute(file_pdf, id, extra_name, string_from_pdf)
    if session:
        dialog_paradigm(id, files)
    else:
        return files


@app.post('/check_project', response_model=ResponsePDF)
def single_pdf(id: int, extra_name: str, request_archive: UploadFile = File(...)):
    try:
        files_names = []
        list_fields = []

        files_pdf, header = ZipAdapter().parse(request_archive, id)

        with ProcessPoolExecutor() as executor:
            for file_pdf in files_pdf:
                string_from_pdf = PDFAdapter().extract(header + '/' + file_pdf)
                if True:
                    future = executor.submit(process_file, file_pdf, id, extra_name, string_from_pdf)
                    # list_fields.extend(future.result())

        shutil.rmtree(header)

    except Exception as e:
        return ResponsePDF(
            id=1111,
            files=[]
        )
    return ResponsePDF(
            id=id,
            files=list_fields
    )