import tkinter as tk
from tkinter import messagebox, filedialog
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


response = requests.get("https://localhost:5000/get_public_key", verify=False)
public_key = RSA.import_key(response.json()['public_key'])
cipher = PKCS1_OAEP.new(public_key)

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Second-Pair Client (User)")
        self.root.geometry("320x280")
        self.server_url = "https://127.0.0.1:5000"
        self.main_menu_frame = tk.Frame(self.root)
        self.login_menu_frame = tk.Frame(self.root)
        self.register_menu_frame = tk.Frame(self.root)
        self.send_receive_frame = tk.Frame(self.root)
        self.upload_content_frame = tk.Frame(self.root)
        self.download_merge_content_frame = tk.Frame(self.root)
        self.username = None
        self.contents = []
        self.user_id = None
        self.init_main_menu_frame()
        self.init_login_menu_frame()
        self.init_register_menu_frame()
        self.init_send_receive_frame()
        self.init_upload_content_frame()
        self.init_download_merge_content_frame()
        self.show_main_menu()

    def init_main_menu_frame(self):
        login_button = tk.Button(self.main_menu_frame, text="Login", command=self.show_login_menu, width=20, height=5)
        register_button = tk.Button(self.main_menu_frame, text="Register", command=self.show_register_menu, width=20, height=5)
        login_button.pack(pady=25)
        register_button.pack(pady=20)

    def init_login_menu_frame(self):
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
        upload_content_button = tk.Button(self.send_receive_frame, text="Upload Content",
                                          command=self.show_upload_content_menu)
        download_merge_content_button = tk.Button(self.send_receive_frame, text="Download/Merge Content",
                                                  command=self.show_download_merge_content_menu)
        exit_button= tk.Button(self.send_receive_frame, text="Exit", command=self.show_main_menu)
        upload_content_button.pack(pady=20)
        download_merge_content_button.pack(pady=20)
        exit_button.pack(pady=20)

    def init_upload_content_frame(self):
        file_label = tk.Label(self.upload_content_frame, text="File")
        self.file_input = tk.Entry(self.upload_content_frame, width=60, justify="center")
        name_label = tk.Label(self.upload_content_frame, text="Name")
        self.name_input = tk.Entry(self.upload_content_frame, width=60, justify="center")
        browse_button = tk.Button(self.upload_content_frame, text="Browse File", command=self.browse_file)
        send_button = tk.Button(self.upload_content_frame, text="Send", command=self.send_content)
        back_button = tk.Button(self.upload_content_frame, text="Back", command=self.show_send_receive_menu)
        file_label.pack(pady=5)
        self.file_input.pack(pady=5)
        name_label.pack(pady=5)
        self.name_input.pack(pady=20)
        browse_button.pack(pady=5)
        send_button.pack(pady=5)
        back_button.pack(pady=5)

    def init_download_merge_content_frame(self):
        content_label = tk.Label(self.download_merge_content_frame, text="Content")
        self.content_list = tk.Listbox(self.download_merge_content_frame, width=60, height=10, justify="center")
        self.refresh_button = tk.Button(self.download_merge_content_frame, text="Refresh Content",
                                        command=self.refresh_content)
        self.download_button = tk.Button(self.download_merge_content_frame, text="Download Selected",
                                         command=self.download_content)
        self.merge_button = tk.Button(self.download_merge_content_frame, text="Merge Audio with Video",
                                      command=self.merge_audio_video)
        back_button = tk.Button(self.download_merge_content_frame, text="Back", command=self.show_send_receive_menu)
        content_label.pack(pady=5)
        self.content_list.pack(pady=20)
        self.refresh_button.pack(pady=5)
        self.download_button.pack(pady=5)
        self.merge_button.pack(pady=5)
        back_button.pack(pady=5)

    def show_main_menu(self):
        self.clear_frames()
        self.main_menu_frame.pack()
        self.root.geometry("320x280")

    def show_login_menu(self):
        self.clear_frames()
        self.login_menu_frame.pack(pady=20)
        self.root.geometry("400x320")

    def show_register_menu(self):
        self.clear_frames()
        self.register_menu_frame.pack(pady=20)
        self.root.geometry("600x420")

    def show_send_receive_menu(self):
        self.clear_frames()
        self.send_receive_frame.pack(pady=50)
        self.root.geometry("320x280")

    def show_upload_content_menu(self):
        self.clear_frames()
        self.upload_content_frame.pack(pady=50)
        self.root.geometry("600x400")

    def show_download_merge_content_menu(self):
        self.refresh_content()
        self.clear_frames()
        self.download_merge_content_frame.pack(pady=50)
        self.root.geometry("600x480")

    def clear_frames(self):
        self.main_menu_frame.pack_forget()
        self.login_menu_frame.pack_forget()
        self.register_menu_frame.pack_forget()
        self.send_receive_frame.pack_forget()
        self.upload_content_frame.pack_forget()
        self.download_merge_content_frame.pack_forget()

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
                self.user_id = response.json()["id"]
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
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 Audio", "*.mp3")])
        if file_path:
            self.file_input.delete(0, tk.END)
            self.file_input.insert(0, file_path)

    def send_content(self):
        file_path = self.file_input.get()
        name = self.name_input.get()
        if not file_path or not name:
            messagebox.showwarning("Error", "Please select a file to upload and the content's name.")
            return
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            payload = {"created_by": str(self.user_id), "creator_type": "user", "name": name}
            response = requests.post(f"{self.server_url}/upload", data=payload, files={"file": content}, verify=False)
            if response.status_code == 201:
                messagebox.showinfo("Success", "File uploaded successfully!")
            else:
                messagebox.showwarning("Error", response.json().get("error", "File upload failed."))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

    def refresh_content(self):
        try:
            response = requests.get(f"{self.server_url}/content", verify=False)
            if response.status_code == 200:
                content = response.json()
                self.content_list.delete(0, tk.END)
                self.contents.clear()
                for item in content:
                    self.content_list.insert(tk.END,f"ID: {item['id']}, Name: {item['name']}, Creator: {item['creator']}")
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
        video_path = filedialog.askopenfilename(title="Select a video file", filetypes=[("MP4 Video", "*.mp4")])
        if video_path:
            video = VideoFileClip(video_path)
            original_audio = video.audio
            audio_path = filedialog.askopenfilename(title="Select an audio file", filetypes=[("MP3 Audio", "*.mp3")])
            file_path = filedialog.asksaveasfilename(title="Save a new video to:", defaultextension=".mp4",
                                                     filetypes=[("MP4 Video", "*.mp4")])
            new_audio = AudioFileClip(audio_path)
            combined_audio = CompositeAudioClip([original_audio, new_audio])
            video_with_audio = video.set_audio(combined_audio)
            video_with_audio.write_videofile(file_path, codec="libx264", audio_codec="aac")
            messagebox.showinfo("Success", "Audio merged with video!")

root = tk.Tk()
client_app = ClientApp(root)
root.mainloop()
