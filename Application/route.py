import logging
from concurrent.futures import ProcessPoolExecutor

import shutil
import stanza
import requests
import fasttext.util
from fastapi import FastAPI

from Adapters.adapters import *
from Application.dialog import dialog_paradigm
from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.ml_models.name_detection.level_1.heuristic import HeuristicModel
from Application.ml_models.name_detection.level_2.fasttext_model import FastTextModel
from Application.ml_models.name_detection.level_3.sbert import SBERTModel
from Application.ml_models.validation.level_1.heuristic import find_string_differences
from Application.pdan import *
from fastapi import FastAPI, UploadFile, File

from Application.pipeline import process_file, get_headers

app = FastAPI(title='MLSER')
logger = logging.getLogger("uvicorn.error")
fasttext.util.download_model('ru')


@app.post('/check_project', response_model=ResponsePDF)
def single_pdf(id: int, extra_name: str, request_archive: UploadFile = File(...)):
    try:
        files_names = []
        list_fields = []

        files_pdf = ZipAdapter().parse(request_archive, id)

        with ProcessPoolExecutor() as executor:
            for file_pdf in files_pdf:
                string_from_pdf = PDFAdapter().extract(file_pdf)
                if True:
                    future = executor.submit(process_file, file_pdf, id, extra_name, string_from_pdf)

    except Exception as e:
        return ResponsePDF(
            id=1111,
            files=[]
        )
    return ResponsePDF(
            id=id,
            files=list_fields
    )


@app.post('/check_project_advance', response_model=ResponsePDF)
def single_pdf(id: int, extra_name: str, config: Configuration, request_archive: UploadFile = File(...)):
    try:
        files_names = []
        list_fields = []
        config = ConfigAdapter().parse(config)

        files_pdf = ZipAdapter().parse(request_archive, id)

        with ProcessPoolExecutor() as executor:
            for file_pdf in files_pdf:
                string_from_pdf = PDFAdapter().extract(file_pdf)
                if True:
                    future = executor.submit(
                        process_file, file_pdf, id, extra_name,
                        string_from_pdf, config.level_detection, False, config)



    except Exception as e:
        return ResponsePDF(
            id=1111,
            files=[]
        )
    return ResponsePDF(
            id=id,
            files=list_fields
    )


@app.post('/get_names_project', response_model=ResponseHypoteticNames)
def search_pdf(id: int, request_archive: UploadFile = File(...)):
    try:
        candidates = []

        files_pdf = ZipAdapter().parse(request_archive, id)

        with ProcessPoolExecutor() as executor:
            for file_pdf in files_pdf:
                string_from_pdf = PDFAdapter().extract(file_pdf, only_one_page=True)
                if True:
                    future = executor.submit(get_headers, string_from_pdf)
                    candidates.extend(future.result())

    except Exception as e:
        raise e
    return ResponseHypoteticNames(
        candidates=candidates
    )