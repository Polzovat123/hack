from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.pdan import Files
from scipy.spatial.distance import cosine


class FastTextModel(ExecuteModel):
    def __init__(self, model):
        self.model = model

    def _fuzzy_find(self, text: str, value: str, max_dist: int = 10) -> list[int]:
        text_std = self._standardize(text)
        value_std = self._standardize(value)
        value_vec = self.model.get_sentence_vector(value_std)

        words = text_std.split()
        combinations = []
        for i in range(len(words) - (max_dist - 1)):
            combination = []
            for j in range(max_dist):
                combination.append(words[i + j])
            emb = self.model.get_sentence_vector(" ".join(combination))
            if 1 - cosine(value_vec, emb)> 0.5:
                combinations.append(i)

        ans = []
        last = -1
        for elem_pos in combinations:
            if last != -1 and last + max_dist > elem_pos:
                pass
            else:
                ans.append(elem_pos)
                last = elem_pos
        return ans

    def execute(self, file_name, folder, correct_name, page_text):
        ans = []

        for page_num, page in enumerate(page_text):
            match_starts = self._fuzzy_find(page, correct_name)
            for elem_add in match_starts:
                print(f'Start on {elem_add} pg:{[page_num]}')
                ans.append(Files(
                    file_name=file_name,
                    folder=folder,
                    name=f'Start on {elem_add}',
                    description='desct',
                    page=page_num
                ))

        return ans