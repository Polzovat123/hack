import requests


def dialog_paradigm(id, files):
    url = f'https://family-clients.ru/older/{id}/send-message'
    requests.post(
        url,
        json={
            'id': int(id),
            'files': files
        }
    )


'''
{
    'id': 123,
    'files': [
        {
            'file_name': '12',
            'folder': '12/1.pdf',
            'name': 'Starts on 45',
            'description': 'Allowed differences:\n',
            'page': 1
        },
        {
            'file_name': '12',
            'folder': '12/1.pdf',
            'name': 'Starts on 34',
            'description': 'Allowed differences:\n',
            'page': 3
        }
    ]
}
'''