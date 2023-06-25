from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.ml_models.validation.level_1.heuristic import find_string_differences
from Application.pdan import Files
from scipy.spatial.distance import cosine
import fasttext.util

class FastTextModel(ExecuteModel):
    def __init__(self, validator):
        super().__init__(validator)
        self.model = fasttext.load_model('cc.ru.300.bin')

    def _fuzzy_find(self, text: str, value: str, max_dist: int = 10):
        text_std = self._standardize(text)
        value_std = self._standardize(value)
        value_vec = self.model.get_sentence_vector(value_std)

        words = text_std.split()
        combinations = []
        reason = []

        for i in range(len(words) - (max_dist - 1)):
            combination = []
            for j in range(max_dist):
                combination.append(words[i + j])
            s = " ".join(combination)
            emb = self.model.get_sentence_vector(s)
            if 1 - cosine(value_vec, emb) > 0.7:
                combinations.append(i)
                reason.append(self._validate_row(value_std, text_std[i: i + len(value_std)]))

        ans = []
        rs = []
        last = -1
        for ind, elem_pos in enumerate(combinations):
            if last != -1 and last + max_dist > elem_pos:
                pass
            else:
                ans.append(elem_pos)
                rs.append(reason[ind])
                last = elem_pos
        return ans, rs

    def execute(self, file_name, folder, correct_name, page_text):
        ans = []

        for page_num, page in enumerate(page_text):
            match_starts, rs = self._fuzzy_find(page, correct_name)
            ans.extend(self._get_new_files(match_starts, file_name, folder, rs, page_num))

        return ans