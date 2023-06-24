import numpy as np
import Levenshtein as lev

from Application.ml_models.name_detection.level_0.interface_model import ExecuteModel
from Application.ml_models.validation.level_1.heuristic import find_string_differences
from Application.pdan import Files


class HeuristicModel(ExecuteModel):

    def _find_local_minima_with_plateau(self, arr, plateau_threshold=0.0):
        minima = []
        n = len(arr)

        for i in range(1, n - 1):
            if arr[i] <= arr[i - 1] and arr[i] <= arr[i + 1]:
                if np.allclose(arr[i], arr[i - 1], atol=plateau_threshold) or np.allclose(arr[i], arr[i + 1],
                                                                                          atol=plateau_threshold):
                    minima.append(i)
                elif arr[i] < np.min([arr[i - 1], arr[i + 1]]):
                    minima.append(i)

        return np.array(minima)

    def _fuzzy_find(self, text: str, value: str, max_dist: int = 10) -> list[int]:
        len_str = len(value)

        text_std = self._standardize(text)
        value_std = self._standardize(value)

        distances = []
        for i in range(1, len(text_std) - len(value_std)):
            distances.append(lev.distance(text_std[i: i + len(value_std)], value_std))

        distances = np.array(distances)
        minima_indecies = self._find_local_minima_with_plateau(distances)
        if (len(minima_indecies) == 0): return []
        filter = distances[minima_indecies] < max_dist

        ans = []
        last = -1
        for elem_pos in minima_indecies[filter]:
            if last != -1 and last + len_str > elem_pos:
                pass
            else:
                ans.append(elem_pos)
                last = elem_pos
        return ans

    def execute(self, file_name, folder, correct_name, page_text):
        ans = []

        for page_num, page in enumerate(page_text):
            match_starts = self._fuzzy_find('перед началом текста '+ page+ ' концовка текста', correct_name)
            for elem_add in match_starts:
                ans.append(Files(
                    file_name=file_name,
                    folder=folder,
                    name=f'Start on {elem_add}',
                    description='rs',
                    page=page_num
                ))
            if (len(match_starts) != 0):
                print([f"Found title on page "
                       f"{page_num:3} char {start:4} "
                       f"{page[start: start + len(correct_name)]}"
                       for start in match_starts])

        return ans