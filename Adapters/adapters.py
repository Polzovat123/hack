import os
import json
import shutil
import zipfile
import pdfplumber


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