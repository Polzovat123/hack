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
    def _check_is_secure(self, path):
        result = subprocess.run(['clamscan', '-r', path], capture_output=True, text=True)
        output = result.stdout.lower()

        if "infected files: 0" in output:
            return True
        else:
            return False

    def parse(self, file, id):
        if not self._check_is_secure(file.filename):
            raise 'Not security zip'

        with open(file.filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        with zipfile.ZipFile(file.filename, "r") as zip_ref:
            zip_ref.extractall(f"source")

        os.remove(file.filename)
        print(f"source/{file.filename[:file.filename.find('.')]}")
        return os.listdir(f"source/{file.filename[:file.filename.find('.')]}"), f"source/{file.filename[:file.filename.find('.')]}"


class PDFAdapter:

    def extract(self, directory: str) -> list[str]:
        pages = []
        i=0
        with pdfplumber.open(directory) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text())
        return pages