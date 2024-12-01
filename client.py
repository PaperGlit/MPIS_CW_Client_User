#Used to make client-to-server requests
import re
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from app_config import server_url

class Client:
    #The class of client-to-server requests
    @staticmethod
    def is_valid_name(name):
        #Checks if the name of the user is valid
        return bool(re.match(r"^[a-zA-Z- ]{1,128}$", name))

    @staticmethod
    def is_valid_username(username):
        #Checks if the username (login) is valid
        return bool(re.match("^[a-zA-Z0-9_]{3,30}$", username))

    @staticmethod
    def is_valid_password(password):
        #Checks if the password is valid
        return bool(re.match("^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&-+=()])(?=\S+$).{8,20}$", password))

    @staticmethod
    def is_valid_email(email):
        #Checks if the email is valid
        return bool(re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

    @staticmethod
    def get_public_key():
        #Gets the public RSA key from the server
        key_response = requests.get(f"{server_url}/auth/get_public_key", verify=False)
        public_key = RSA.import_key(key_response.json()['public_key'])
        cipher = PKCS1_OAEP.new(public_key)
        return cipher

    @staticmethod
    def login(username, password):
        #Makes a login request
        if not Client.is_valid_username(username) or not Client.is_valid_password(password):
            raise ValueError("Invalid username or password")
        cipher = Client.get_public_key()
        encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
        encrypted_password = base64.b64encode(cipher.encrypt(password.encode())).decode()
        payload = {"username": encrypted_username, "password": encrypted_password}
        try:
            response = requests.post(f"{server_url}/auth/login", json=payload, verify=False)
            if response.status_code == 200:
                user_id = response.json()["id"]
                return user_id
            else:
                raise Exception("An error occurred: " + response.json()["status"])
        except Exception as e:
            raise Exception("An error occurred: " + str(e))

    @staticmethod
    def register(name, username, password, email):
        #Makes a register request
        if (not Client.is_valid_name(name) or not Client.is_valid_username(username)
                or not Client.is_valid_password(password) or not Client.is_valid_email(email)):
            raise ValueError("Invalid data, please try again")
        cipher = Client.get_public_key()
        encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
        encrypted_password = base64.b64encode(cipher.encrypt(password.encode())).decode()
        payload = {"name": name, "username": encrypted_username, "password": encrypted_password, "email": email}
        try:
            response = requests.post(f"{server_url}/auth/register", json=payload, verify=False)
            if response.status_code == 201:
                return True
            else:
                raise Exception("An error occurred: " + response.json()["status"])
        except Exception as e:
            raise Exception("An error occurred: " + str(e))

    @staticmethod
    def send_content(file_path, name, user_id):
        #Uploads content to the server
        if not file_path or not name:
            raise ValueError("Please select a file to upload and the content's name.")
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            payload = {"created_by": str(user_id), "creator_type": "user", "name": name}
            response = requests.post(f"{server_url}/content/upload", data=payload, files={"file": content}, verify=False)
            if response.status_code == 201:
                return True
            else:
                raise Exception("An error occurred: " + response.json()["status"])
        except Exception as e:
            raise Exception("An error occurred: " + str(e))

    @staticmethod
    def refresh_content():
        #Refreshed the list of content available
        try:
            response = requests.get(f"{server_url}/content/refresh", verify=False)
            return response.json()
        except Exception as e:
            raise Exception("An error occurred: " + str(e))

    @staticmethod
    def download_content(content):
        #Downloads the content from the server
        content_id = content.get("id")
        try:
            response = requests.get(f"{server_url}/content/download/{content_id}", stream=True, verify=False)
            if response.status_code == 200:
                return response.iter_content(chunk_size=8192)
            else:
                raise Exception("Failed to download content.")
        except Exception as e:
            raise Exception("An error occurred: " + str(e))
