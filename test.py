# import requests
#
# # Open the file to be uploaded
# file_path = r'D:\12.zip'
# with open(file_path, 'rb') as file:
#     files = {'archive': (file.name, file)}
#
#     # Create the request data dictionary
#     data = {
#         'id': 12,
#         'extra_name': 'qweqweqw',
#         # 'archive': open(r'D:\12.zip', 'rb')
#     }
#
#     # Send the request
#     response = requests.post(
#         'http://127.0.0.1:6432/check_project',
#         json=data)
#
# # Print the response
# print(response.json())
import requests

# Set the endpoint URL
url = 'http://localhost:6432/check_project'

# Prepare the request data
data = {
    'id': 123,
    'extra_name': 'example_name',
}

# Set the file path of the archive to be uploaded
file_path = f'D:/12.zip'

# Create the files dictionary
files = {
    'request_archive': open(file_path, 'rb')
}

# Send the request
response = requests.post(url, data=data, files=files)

# Print the response
print(response.json())

