import os
import json
import shutil
import zipfile
import pdfplumber
import subprocess

from Entity.config import ConfigCompute


class ConfigAdapter:
    def parse(self, json_entity):
        json_entity = json.load(json_entity)
        level_detection = json_entity['level_detection']
        name_img_parser = json_entity['img_model']['name_model']
        level_using = json_entity['img_model']['level_using']
        name_validator = json_entity['validator_model']['name_model']

        return ConfigCompute(
            level_detection, name_img_parser,
            level_using, name_validator
        )


class JSONAdapter:
    def parse(self, json_file, archive):
        json_ans = json.load(json_file)
        # id = json_ans['id']
        # extra_name = json_ans['extra_name']
        archive = archive
        # return id, extra_name, archive

class ZipAdapter:
    def parse(self, file, id):
        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with zipfile.ZipFile(file.filename, "r") as zip_ref:
            zip_ref.extractall(f"source/{id}")
            # zip_ref.extractall(f"source")

        os.remove(file.filename)
        # return os.listdir("..")
        print(f"source/{file.filename[:file.filename.find('.')]}")
        return os.listdir(f"source/{id}"), f"source/{id}"
class PDFAdapter:

    def extract(self, path: str, only_one_page=False) -> list[str]:
        pages = []
        i=0
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text())
                if only_one_page:
                    break
        return pages