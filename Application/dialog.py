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