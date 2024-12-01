#Creates and interactable graphic user interface
import tkinter as tk
from tkinter import messagebox, filedialog
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from client import Client


class GUI:
    #The class that creates the gui
    def __init__(self, root):
        #Initiate window
        self.root = root
        self.root.title("Second-Pair Client (User)")
        self.root.geometry("320x280")

        #Initiate GUI frames (first part)
        self.main_menu_frame = tk.Frame(self.root)
        self.login_menu_frame = tk.Frame(self.root)
        self.register_menu_frame = tk.Frame(self.root)
        self.send_receive_frame = tk.Frame(self.root)
        self.upload_content_frame = tk.Frame(self.root)
        self.download_merge_content_frame = tk.Frame(self.root)

        #Initiate GUI elements
        self.login_username_input = None
        self.login_password_input = None
        self.register_name_input = None
        self.register_username_input = None
        self.register_password_input = None
        self.register_email_input = None
        self.file_input = None
        self.file_name_input = None
        self.content_list = None
        self.refresh_button = None
        self.download_button = None
        self.merge_button = None

        #Initiate reusable variables
        self.user_id = None
        self.contents = []

        #Initiate GUI frames (second part)
        self.init_main_menu_frame()
        self.init_login_menu_frame()
        self.init_register_menu_frame()
        self.init_send_receive_frame()
        self.init_upload_content_frame()
        self.init_download_merge_content_frame()
        self.show_main_menu()

    def init_main_menu_frame(self):
        #Initiates main menu frame
        login_button = tk.Button(self.main_menu_frame, text="Login", command=self.show_login_menu, width=20, height=5)
        register_button = tk.Button(self.main_menu_frame, text="Register", command=self.show_register_menu, width=20, height=5)
        login_button.pack(pady=25)
        register_button.pack(pady=20)

    def init_login_menu_frame(self):
        #Initiates login menu frame
        username_label = tk.Label(self.login_menu_frame, text="Username")
        self.login_username_input = tk.Entry(self.login_menu_frame)
        password_label = tk.Label(self.login_menu_frame, text="Password")
        self.login_password_input = tk.Entry(self.login_menu_frame, show="*")
        login_button = tk.Button(self.login_menu_frame, text="Login", command=self.login)
        back_button = tk.Button(self.login_menu_frame, text="Back to Main Menu", command=self.show_main_menu)
        username_label.pack(pady=5)
        self.login_username_input.pack(pady=5)
        password_label.pack(pady=5)
        self.login_password_input.pack(pady=5)
        login_button.pack(pady=20)
        back_button.pack(pady=20)

    def init_register_menu_frame(self):
        #Initiates register menu frame
        name_label = tk.Label(self.register_menu_frame, text="Name")
        self.register_name_input = tk.Entry(self.register_menu_frame)
        username_label = tk.Label(self.register_menu_frame, text="Username")
        self.register_username_input = tk.Entry(self.register_menu_frame)
        password_label = tk.Label(self.register_menu_frame, text="Password")
        self.register_password_input = tk.Entry(self.register_menu_frame, show="*")
        email_label = tk.Label(self.register_menu_frame, text="Email")
        self.register_email_input = tk.Entry(self.register_menu_frame)
        register_button = tk.Button(self.register_menu_frame, text="Register", command=self.register)
        back_button = tk.Button(self.register_menu_frame, text="Back to Main Menu", command=self.show_main_menu)
        name_label.pack(pady=5)
        self.register_name_input.pack(pady=5)
        username_label.pack(pady=5)
        self.register_username_input.pack(pady=5)
        password_label.pack(pady=5)
        self.register_password_input.pack(pady=5)
        email_label.pack(pady=5)
        self.register_email_input.pack(pady=5)
        register_button.pack(pady=20)
        back_button.pack(pady=20)

    def init_send_receive_frame(self):
        #Initiates send-receive frame
        upload_content_button = tk.Button(self.send_receive_frame, text="Upload Content",
                                          command=self.show_upload_content_menu)
        download_merge_content_button = tk.Button(self.send_receive_frame, text="Download/Merge Content",
                                                  command=self.show_download_merge_content_menu)
        exit_button= tk.Button(self.send_receive_frame, text="Exit", command=self.show_main_menu)
        upload_content_button.pack(pady=20)
        download_merge_content_button.pack(pady=20)
        exit_button.pack(pady=20)

    def init_upload_content_frame(self):
        #Initiates upload content frame
        file_label = tk.Label(self.upload_content_frame, text="File")
        self.file_input = tk.Entry(self.upload_content_frame, width=60, justify="center")
        name_label = tk.Label(self.upload_content_frame, text="Name")
        self.file_name_input = tk.Entry(self.upload_content_frame, width=60, justify="center")
        browse_button = tk.Button(self.upload_content_frame, text="Browse File", command=self.browse_file)
        send_button = tk.Button(self.upload_content_frame, text="Send", command=self.send_content)
        back_button = tk.Button(self.upload_content_frame, text="Back", command=self.show_send_receive_menu)
        file_label.pack(pady=5)
        self.file_input.pack(pady=5)
        name_label.pack(pady=5)
        self.file_name_input.pack(pady=20)
        browse_button.pack(pady=5)
        send_button.pack(pady=5)
        back_button.pack(pady=5)

    def init_download_merge_content_frame(self):
        #Initiates download-merge content frame
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
        #Allows user to register or log into the server
        self.login_menu_frame.pack_forget()
        self.register_menu_frame.pack_forget()
        self.send_receive_frame.pack_forget()
        self.main_menu_frame.pack()
        self.root.geometry("320x280")

    def show_login_menu(self):
        #Manu that allows user to log into the server
        self.main_menu_frame.pack_forget()
        self.login_menu_frame.pack(pady=20)
        self.root.geometry("400x320")

    def show_register_menu(self):
        #Menu that allows user to register on the server
        self.main_menu_frame.pack_forget()
        self.register_menu_frame.pack(pady=20)
        self.root.geometry("600x420")

    def show_send_receive_menu(self):
        #Menu that allows user to choose between uploading and downloading content
        self.login_menu_frame.pack_forget()
        self.upload_content_frame.pack_forget()
        self.download_merge_content_frame.pack_forget()
        self.send_receive_frame.pack(pady=20)
        self.root.geometry("320x280")

    def show_upload_content_menu(self):
        #Menu that allows user to send content to the server
        self.send_receive_frame.pack_forget()
        self.upload_content_frame.pack(pady=50)
        self.root.geometry("600x400")

    def show_download_merge_content_menu(self):
        #Menu that allows user to download content and merge it with videos
        self.refresh_content()
        self.send_receive_frame.pack_forget()
        self.download_merge_content_frame.pack(pady=50)
        self.root.geometry("600x480")

    def login(self):
        #Logs user into the server
        username = self.login_username_input.get()
        password = self.login_password_input.get()
        try:
            self.user_id = Client.login(username, password)
            self.show_send_receive_menu()
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def register(self):
        #Registers user on the server
        name = self.register_name_input.get()
        username = self.register_username_input.get()
        password = self.register_password_input.get()
        email = self.register_email_input.get()
        try:
            if Client.register(name, username, password, email):
                messagebox.showinfo("Success", "Registration successful! You can now log in.")
                self.show_login_menu()
        except Exception as e:
            messagebox.showerror("Registration Failed", str(e))

    def browse_file(self):
        #Used to select content to upload to the server
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 Audio", "*.mp3")])
        if file_path:
            self.file_input.delete(0, tk.END)
            self.file_input.insert(0, file_path)

    def send_content(self):
        #Sends content to the server
        file_path = self.file_input.get()
        name = self.file_name_input.get()
        try:
            if Client.send_content(file_path, name, self.user_id):
                messagebox.showinfo("Success", "File uploaded successfully!")
        except ValueError as e:
            messagebox.showwarning("Error", str(e))
        except Exception as e:
            messagebox.showerror("Upload Failed", str(e))

    def refresh_content(self):
        #Refreshes the list of available content
        try:
            content = Client.refresh_content()
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
        #Downloads the content as .mp3 files
        selected = self.content_list.curselection()
        if not selected:
            messagebox.showwarning("Error", "Please select content to download.")
            return
        content = self.contents[selected[0]]
        try:
            downloaded_file = Client.download_content(content)
            file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Audio", "*.mp3")])
            if file_path:
                with open(file_path, 'wb') as f:
                    for chunk in downloaded_file:
                        f.write(chunk)
                messagebox.showinfo("Success", f"Content downloaded to: {file_path}")
            else:
                messagebox.showwarning("Error", "Download location not specified.")
        except Exception as e:
            messagebox.showwarning("Error", f"Failed to download content: {e}")
            return

    @staticmethod
    def merge_audio_video():
        #Merges selected video's audio track with selected audio file
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
