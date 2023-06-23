from Application.pdan import Files


class ExecuteModel:
    def _standardize(self, string: str) -> str:
        return string.lower().replace('\n', ' ').replace('  ', ' ')

    def execute(self, file_name, folder, correct_name, page_text):
        ans = []
        if True:
            ans.append(Files(
                file_name=file_name,
                folder=folder,
                name='error in first letter',
                description='desct',
                page=0
            ))
        return ans


