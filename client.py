import ast
import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


# Fetch public key from the server
response = requests.get("https://localhost:5000/get_public_key", verify=False)
public_key = RSA.import_key(response.json()['public_key'])
cipher = PKCS1_OAEP.new(public_key)


class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Second-Pair Client (User)")
        self.root.geometry("320x280")

        # Server URL
        self.server_url = "https://127.0.0.1:5000"

        # Frames
        self.main_menu_frame = tk.Frame(self.root)
        self.login_menu_frame = tk.Frame(self.root)
        self.register_menu_frame = tk.Frame(self.root)
        self.send_receive_frame = tk.Frame(self.root)
        self.upload_content_frame = tk.Frame(self.root)
        self.download_merge_content_frame = tk.Frame(self.root)

        self.username = None
        self.contents = []

        # Initialize frames
        self.init_main_menu_frame()
        self.init_login_menu_frame()
        self.init_register_menu_frame()
        self.init_send_receive_frame()
        self.init_upload_content_frame()
        self.init_download_merge_content_frame()

        self.main_menu_frame.pack()

    def init_main_menu_frame(self):
        # Main menu layout (Login / Register buttons)
        login_button = tk.Button(self.main_menu_frame, text="Login", command=self.show_login_menu)
        register_button = tk.Button(self.main_menu_frame, text="Register", command=self.show_register_menu)

        login_button.pack(pady=60)
        register_button.pack(pady=20)

    def init_login_menu_frame(self):
        # Login menu layout (Login Form)
        username_label = tk.Label(self.login_menu_frame, text="Username")
        self.username_input = tk.Entry(self.login_menu_frame)

        password_label = tk.Label(self.login_menu_frame, text="Password")
        self.password_input = tk.Entry(self.login_menu_frame, show="*")

        login_button = tk.Button(self.login_menu_frame, text="Login", command=self.login)
        back_button = tk.Button(self.login_menu_frame, text="Back to Main Menu", command=self.show_main_menu)

        username_label.pack(pady=5)
        self.username_input.pack(pady=5)
        password_label.pack(pady=5)
        self.password_input.pack(pady=5)

        login_button.pack(pady=20)
        back_button.pack(pady=20)

    def init_register_menu_frame(self):
        # Register menu layout (Register Form)
        name_label = tk.Label(self.register_menu_frame, text="Name")
        self.name_input = tk.Entry(self.register_menu_frame)

        username_label = tk.Label(self.register_menu_frame, text="Username")
        self.register_username_input = tk.Entry(self.register_menu_frame)

        password_label = tk.Label(self.register_menu_frame, text="Password")
        self.register_password_input = tk.Entry(self.register_menu_frame, show="*")

        email_label = tk.Label(self.register_menu_frame, text="Email")
        self.email_input = tk.Entry(self.register_menu_frame)

        register_button = tk.Button(self.register_menu_frame, text="Register", command=self.register)
        back_button = tk.Button(self.register_menu_frame, text="Back to Main Menu", command=self.show_main_menu)

        name_label.pack(pady=5)
        self.name_input.pack(pady=5)
        username_label.pack(pady=5)
        self.register_username_input.pack(pady=5)
        password_label.pack(pady=5)
        self.register_password_input.pack(pady=5)
        email_label.pack(pady=5)
        self.email_input.pack(pady=5)

        register_button.pack(pady=20)
        back_button.pack(pady=20)

    def init_send_receive_frame(self):
        # Send/Receive Content menu layout
        upload_content_button = tk.Button(self.send_receive_frame, text="Upload Content", command=self.show_upload_content_menu)
        download_merge_content_button = tk.Button(self.send_receive_frame, text="Download/Merge Content", command=self.show_download_merge_content_menu)

        upload_content_button.pack(pady=20)
        download_merge_content_button.pack(pady=20)

    def init_upload_content_frame(self):
        # Upload content menu layout
        self.file_input = tk.Entry(self.upload_content_frame)
        browse_button = tk.Button(self.upload_content_frame, text="Browse File", command=self.browse_file)
        send_button = tk.Button(self.upload_content_frame, text="Send", command=self.send_content)
        back_button = tk.Button(self.upload_content_frame, text="Back", command=self.show_send_receive_menu)

        self.file_input.pack(pady=5)
        browse_button.pack(pady=5)
        send_button.pack(pady=20)
        back_button.pack(pady=20)

    def init_download_merge_content_frame(self):
        # Download/Merge content menu layout
        self.content_list = tk.Listbox(self.download_merge_content_frame)
        self.refresh_button = tk.Button(self.download_merge_content_frame, text="Refresh Content", command=self.refresh_content)
        self.download_button = tk.Button(self.download_merge_content_frame, text="Download Selected", command=self.download_content)
        self.merge_button = tk.Button(self.download_merge_content_frame, text="Merge Audio with Video", command=self.merge_audio_video)
        back_button = tk.Button(self.download_merge_content_frame, text="Back", command=self.show_send_receive_menu)

        self.refresh_content()

        self.content_list.pack(pady=10)
        self.refresh_button.pack(pady=10)
        self.download_button.pack(pady=10)
        self.merge_button.pack(pady=10)
        back_button.pack(pady=20)

    def show_main_menu(self):
        # Show main menu
        self.login_menu_frame.pack_forget()
        self.register_menu_frame.pack_forget()
        self.send_receive_frame.pack_forget()
        self.upload_content_frame.pack_forget()
        self.download_merge_content_frame.pack_forget()
        self.main_menu_frame.pack()
        self.root.geometry("800x600")  # Main menu window size

    def show_login_menu(self):
        # Show login menu
        self.main_menu_frame.pack_forget()
        self.register_menu_frame.pack_forget()
        self.send_receive_frame.pack_forget()
        self.upload_content_frame.pack_forget()
        self.download_merge_content_frame.pack_forget()
        self.login_menu_frame.pack(pady=50)
        self.root.geometry("400x300")  # Smaller window for login

    def show_register_menu(self):
        # Show register menu
        self.main_menu_frame.pack_forget()
        self.login_menu_frame.pack_forget()
        self.send_receive_frame.pack_forget()
        self.upload_content_frame.pack_forget()
        self.download_merge_content_frame.pack_forget()
        self.register_menu_frame.pack(pady=50)
        self.root.geometry("600x400")  # Larger window for register

    def show_send_receive_menu(self):
        # Show send/receive menu
        self.upload_content_frame.pack_forget()
        self.download_merge_content_frame.pack_forget()
        self.send_receive_frame.pack(pady=50)
        self.root.geometry("800x600")  # Adjust size for send/receive menu

    def show_upload_content_menu(self):
        # Show upload content menu
        self.send_receive_frame.pack_forget()
        self.upload_content_frame.pack(pady=50)
        self.root.geometry("600x400")  # Adjust size for upload

    def show_download_merge_content_menu(self):
        # Show download/merge content menu
        self.send_receive_frame.pack_forget()
        self.download_merge_content_frame.pack(pady=50)
        self.root.geometry("800x600")  # Adjust size for download/merge

    def login(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if not username or not password:
            messagebox.showwarning("Error", "Username and password are required!")
            return

        encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
        encrypted_password = base64.b64encode(cipher.encrypt(password.encode())).decode()

        payload = {"username": encrypted_username, "password": encrypted_password}
        try:
            response = requests.post(f"{self.server_url}/login", json=payload, verify=False)
            if response.status_code == 200:
                self.username = username
                self.show_send_receive_menu()
            else:
                messagebox.showwarning("Error", response.json().get("error", "Login failed."))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def register(self):
        name = self.name_input.get()
        username = self.register_username_input.get()
        password = self.register_password_input.get()
        email = self.email_input.get()

        if not name or not username or not password or not email:
            messagebox.showwarning("Error", "All fields are required!")
            return

        encrypted_username = base64.b64encode(cipher.encrypt(username.encode())).decode()
        encrypted_password = base64.b64encode(cipher.encrypt(password.encode())).decode()
        payload = {"name": name, "username": encrypted_username, "password": encrypted_password, "email": email}
        try:
            response = requests.post(f"{self.server_url}/register", json=payload, verify=False)
            if response.status_code == 201:
                messagebox.showinfo("Success", "Registration successful! You can now log in.")
                self.show_login_menu()
            else:
                messagebox.showwarning("Error", response.json().get("error", "Registration failed."))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to server: {e}")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_input.delete(0, tk.END)
            self.file_input.insert(0, file_path)

    def send_content(self):
        file_path = self.file_input.get()
        if not file_path:
            messagebox.showwarning("Error", "Please select a file to upload.")
            return

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            response = requests.post(f"{self.server_url}/upload", files={"file": content}, verify=False)
            if response.status_code == 200:
                messagebox.showinfo("Success", "File uploaded successfully!")
            else:
                messagebox.showwarning("Error", response.json().get("error", "File upload failed."))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

    def refresh_content(self):
        # Fetch content list from the server
        try:
            response = requests.get(f"{self.server_url}/content", verify=False)
            if response.status_code == 200:
                content = response.json()
                self.content_list.delete(0, tk.END)
                self.contents.clear()
                for item in content:
                    self.content_list.insert(tk.END,f"ID: {item['id']}, Name: {item['name']}, Creator: {item['creator_type']}")
                    self.contents.append(item)
            else:
                messagebox.showwarning("Error", "Failed to load content.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch content: {e}")

    def download_content(self):
        selected = self.content_list.curselection()
        if not selected:
            messagebox.showwarning("Error", "Please select content to download.")
            return
        content = self.contents[selected[0]]
        content_id = content.get("id")
        try:
            response = requests.get(f"{self.server_url}/download/{content_id}", stream=True, verify=False)
            if response.status_code == 200:
                file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Audio", "*.mp3")])
                if file_path:
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    messagebox.showinfo("Success", f"Content downloaded to: {file_path}")
                else:
                    messagebox.showwarning("Error", "Download location not specified.")
            else:
                messagebox.showwarning("Error", "Failed to download content.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download content: {e}")

    def merge_audio_video(self):
        selected = self.content_list.curselection()
        if not selected:
            messagebox.showwarning("Error", "Please select a video to merge.")
            return
        content_name = self.content_list.get(selected[0])
        # Logic for merging video and audio here
        messagebox.showinfo("Success", f"Merged audio with {content_name}")


# Create the Tkinter root window
root = tk.Tk()
client_app = ClientApp(root)
root.mainloop()
