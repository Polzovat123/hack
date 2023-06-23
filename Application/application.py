from Application.pdan import Files


class ExecuteModel:
    def execute(self, file_name, page, folder, correct_name):
        ans = []
        if True:
            ans.append(Files(
                file_name=file_name,
                folder=folder,
                name='error in first letter',
                description='desct',
                page=page
            ))
        return ans