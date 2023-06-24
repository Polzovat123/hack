import stanza

from Application.dialog import dialog_paradigm
from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.ml_models.name_detection.level_1.heuristic import HeuristicModel
from Application.ml_models.name_detection.level_2.fasttext_model import FastTextModel
from Application.ml_models.name_detection.level_3.sbert import SBERTModel
from Application.ml_models.name_recognition.level_3.stanza import StanzaNameRecognition
from Application.ml_models.validation.level_1.heuristic import find_string_differences
from Application.pdan import Files


def process_file(file_pdf, id, extra_name, string_from_pdf, level_naming_detection=1, session=False, config=None):
    if config is None:
        if level_naming_detection == 1:
            print('heuristic')
            # files = HeuristicModel(find_string_differences).execute(file_pdf, id, extra_name, string_from_pdf)
            files = [(Files(
                file_name='1.pdf',
                folder='12',
                name=f'Start on {34}',
                description='Incorrect input',
                page=1
            ))]
        elif level_naming_detection == 2:
            files = FastTextModel(find_string_differences).execute(file_pdf, id, extra_name, string_from_pdf)
        elif level_naming_detection == 3:
            files = SBERTModel(find_string_differences).execute(file_pdf, id, extra_name, string_from_pdf)
        else:
            print('interface')
            files = ExecuteModel(find_string_differences).execute(file_pdf, id, extra_name, string_from_pdf)
        if session:
            dialog_paradigm(id, files)
        else:
            return files
    else:
        validator_name = config.config_validator.name_model
        if validator_name == 'default':
            validator = find_string_differences
        else:
            validator = find_string_differences

        if level_naming_detection == 1:
            files = HeuristicModel(validator).execute(file_pdf, id, extra_name, string_from_pdf)
        elif level_naming_detection == 2:
            files = FastTextModel(validator).execute(file_pdf, id, extra_name, string_from_pdf)
        elif level_naming_detection == 3:
            files = SBERTModel(validator).execute(file_pdf, id, extra_name, string_from_pdf, 0.7)
        else:
            files = ExecuteModel(validator).execute(file_pdf, id, extra_name, string_from_pdf)


    if session:
        dialog_paradigm(id, files)
    else:
        return files


def get_headers(string_from_pdf, config=None):
    candidates_headers = []
    stanza.download('ru')
    nlp = stanza.Pipeline('ru')

    if config is None:
        candidates_headers.extend(StanzaNameRecognition(nlp).extract_organizations(string_from_pdf[0]))

    return candidates_headers