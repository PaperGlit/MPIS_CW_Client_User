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

# Fetch public key from server
respons = requests.get("https://localhost:5000/get_public_key", verify=False)
public_key = RSA.import_key(respons.json()['public_key'])
cipher = PKCS1_OAEP.new(public_key)

# Register
def register(username, password):
    encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
    payload = {
        "username": encrypted_username,
        "password": password  # Ensure password is correctly passed
    }
    response = requests.post("https://localhost:5000/register", json=payload, verify=False)
    print(response.json())

# Login
def login(username, password):
    encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
    payload = {
        "username": encrypted_username,
        "password": password
    }
    response = requests.post("https://localhost:5000/login", json=payload, verify=False)
    print(response.json())

import requests

# Fetch all content
def get_all_content():
    url = 'https://127.0.0.1:5000/get_all_content'
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        content_list = response.json()
        for content in content_list:
            print(f"ID: {content['id']}, Name: {content['name']}, Creator: {content['creator_type']}")
        return content_list
    else:
        print("Error:", response.json())

# Download a specific content file
def download_content(content_id):
    url = f'https://127.0.0.1:5000/download_audio/{content_id}'
    response = requests.get(url, stream=True, verify=False)
    if response.status_code == 200:
        with open(f'content_{content_id}.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded content_{content_id}.mp3")
    else:
        print("Error:", response.json())

# Example usage
# Fetch all content
content_list = get_all_content()

# Download content with a specific ID (e.g., ID = 1)
if content_list:
    download_content(content_list[0]['id'])  # Change index or provide ID directly

#Example usage
# register("testuser", "securepassword")
# login("testuser", "securepassword")
# upload_audio()