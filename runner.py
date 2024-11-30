import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64


def upload_audio():
    url = 'https://127.0.0.1:5000/upload_audio'
    file_path = 'example_audio.mp3'
    data = {
        'created_by': '1',             # ID of the user/worker uploading the file
        'creator_type': 'user',        # Either 'user' or 'worker'
        'name': 'Sample Audio File'    # Name of the content
    }
    files = {
        'file': open(file_path, 'rb')  # Open the audio file in binary mode
    }
    response = requests.post(url, data=data, files=files, verify=False)
    if response.status_code == 201:
        print("Upload successful:", response.json())
    else:
        print("Error:", response.json())

# # Fetch public key from server
# respons = requests.get("https://localhost:5000/get_public_key", verify=False)
# public_key = RSA.import_key(respons.json()['public_key'])
# cipher = PKCS1_OAEP.new(public_key)

# # Register
# def register(username, password):
#     encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
#     payload = {
#         "username": encrypted_username,
#         "password": password
#     }
#     response = requests.post("https://localhost:5000/register", json=payload, verify=False)
#     print(response.json())
#
# # Login
# def login(username, password):
#     encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
#     payload = {
#         "username": encrypted_username,
#         "password": password
#     }
#     response = requests.post("https://localhost:5000/login", json=payload, verify=False)
#     print(response.json())

# Example usage
# register("testuser", "securepassword")
# login("testuser", "securepassword")
upload_audio()