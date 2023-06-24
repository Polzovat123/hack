import os

from Application.pdan import Files


class ExecuteModel:
    def __init__(self, validator):
        self.validate = validator

    def _standardize(self, string: str) -> str:
        return string.lower().replace('\n', ' ').replace('  ', ' ')

    def _validate_row(self, target, text):
        allowed, not_allowed = self.validate(
            target, text
        )
        rs = "Allowed differences:\n"
        for diff in allowed:
            rs = rs + f"  - {diff}\n"

        rs = rs + "\nUnallowed differences:\n"
        for diff in not_allowed:
            rs = rs + f"  - {diff}\n"
        return rs

    def _get_new_files(self, match_starts, file_path, folder, rs, page_num):
        ans = []
        for elem_add in match_starts:
            directory = os.path.dirname(file_path)
            filename = os.path.basename(file_path)
            ans.append(Files(
                file_name=filename,
                folder=directory,
                name=f'Start on {elem_add}',
                description=rs[0],
                page=page_num
            ))
        return ans

    def execute(self, file_name, folder, correct_name, page_text):
        ans = []
        if True:
            print(file_name)
            print(self._get_new_files([12, 43], file_name, folder, ['error', 'error2'], 0))
            raise 'I broke'
            ans.extend(self._get_new_files([12, 43], file_name, folder, ['error', 'error2'], 0))
        return ans


