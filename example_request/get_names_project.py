import time

import requests

# Set the endpoint URL
url_i = 'http://178.205.138.31:6432/get_names_project'
url = 'http://127:0.0.1:6432/check_project'

# Prepare the request data
data = {
    'id': 123,
}

# Set the file path of the archive to be uploaded
file_path = f'D:/12.zip'

# Create the files dictionary
files = {
    'request_archive': open(file_path, 'rb')
}

start_time = time.time()
response = requests.post(url_i, params=data, files=files)
end_time = time.time()
request_time = end_time - start_time
print(f"Время выполнения запроса: {request_time} секунд")
print(response.json())

