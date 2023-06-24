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

    def _get_new_files(self, match_starts, file_name, folder, rs, page_num):
        ans = []
        for elem_add in match_starts:
            ans.append(Files(
                file_name=file_name,
                folder=str(folder),
                name=f'Start on {elem_add}',
                description=rs[0],
                page=page_num
            ))
        return ans

    def execute(self, file_name, folder, correct_name, page_text):
        ans = []
        if True:
            ans.extend(self._get_new_files([], file_name, folder, [], 0))
        return ans


