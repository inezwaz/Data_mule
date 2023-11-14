import tkinter as tk
from tkinter import ttk, filedialog
import json
import hashlib
import os
import re
#gui

class App:

    def load_login_info(self):
        try:
            with open("login_info.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def __init__(self, root):
        self.root = root
        self.root.title("File Storage App")

        # Set the window size and center it
        window_width = 600
        window_height = 400
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        self.root.geometry(
            f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Current user
        self.current_user = None

        # Load login information from the JSON file
        self.login_info = self.load_login_info()

        # Login Page
        self.login_frame = ttk.Frame(self.root, padding="10")
        self.create_login_page()

        # Registration Page
        self.registration_frame = ttk.Frame(self.root, padding="10")
        self.create_registration_page()

        # Dropbox-like Page
        self.dropbox_frame = ttk.Frame(self.root, padding="10")
        self.create_dropbox_page()

        # Load friend list from the JSON file
        self.friend_list = self.load_friend_list()

        # Load uploaded files from the JSON file
        self.uploaded_files = self.load_uploaded_files()

        # Friend List Page
        self.friend_list_frame = ttk.Frame(self.root, padding="10")
        self.create_friend_list_page()

        # Download Files Page
        self.download_files_frame = ttk.Frame(self.root, padding="10")
        self.create_download_files_page()

        # Initially, show the login page
        self.show_login_page()

        # Add a status label to the Dropbox page
        #self.file_transfer_status_label = ttk.Label(self.dropbox_frame, text="", background="white")
        #self.file_transfer_status_label.grid(row=5, column=0, columnspan=2, pady=5)

        # Add a listbox for file statuses
        self.file_status_listbox = tk.Listbox(self.dropbox_frame, height=10)
        self.file_status_listbox.grid(row=7, column=0, columnspan=2, padx=20, sticky=(tk.W, tk.E))

        # Add a button to refresh file statuses
        self.refresh_status_button = ttk.Button(self.dropbox_frame, text="Refresh Statuses", command=self.refresh_file_statuses)
        self.refresh_status_button.grid(row=8, column=0, columnspan=2, pady=5)

        
    def get_file_statuses(self, log_file_path, directory_path):
        file_statuses = {}

        def update_file_status(filename, status):
            file_statuses[filename] = status

        def get_status(line):
            if "download" in line:
                return "In Transit (Yellow)"
            elif "upload" in line:
                return "Delivered (Green)"
            else:
                return "Other (Gray)"

        # Read log file and update statuses
        with open(log_file_path, 'r') as log_file:
            download_pattern = re.compile(r"download (.+?) to")
            upload_pattern = re.compile(r"upload (.+?) to")

            for line in log_file:
                if ".log" in line:
                    continue

                status = get_status(line)
                download_match = download_pattern.search(line)
                upload_match = upload_pattern.search(line)

                if download_match:
                    filename = download_match.group(1)
                elif upload_match:
                    filename = upload_match.group(1)
                else:
                    continue

                update_file_status(filename, status)

        # List files in the directory
        files_in_directory = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        # Compare and update file statuses
        for file in files_in_directory:
            if file not in file_statuses:
                file_statuses[file] = "Not in Log (Gray)"

        return file_statuses    
    

    def refresh_file_statuses(self):
        # Clear the current list
        self.file_status_listbox.delete(0, tk.END)

        # Define the paths for the log file and directory
        log_file_path = r'C:\Users\newti\Desktop\FTPfolder\client.log'
        directory_path = r'C:\Users\newti\Desktop\FTPfolder'

        # Get the file statuses
        status_dict = self.get_file_statuses(log_file_path, directory_path)

        # Update the listbox with new statuses
        for filename, status in status_dict.items():
            self.file_status_listbox.insert(tk.END, f"{filename}: {status}")


    def create_login_page(self):
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.welcome_label_login = ttk.Label(
            self.login_frame, text="Welcome to Data Depot", font=("Helvetica", 16))
        self.username_label = ttk.Label(self.login_frame, text="Username:")
        self.password_label = ttk.Label(self.login_frame, text="Password:")
        self.username_entry = ttk.Entry(self.login_frame)
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.login_button = ttk.Button(
            self.login_frame, text="Login", command=self.login)
        self.create_account_button = ttk.Button(
            self.login_frame, text="Create Account", command=self.show_registration_page)

        self.login_frame.columnconfigure(1, weight=1)
        for i in range(5):
            self.login_frame.rowconfigure(i, weight=1)

        padding_x = 40
        padding_y = 5

        self.welcome_label_login.grid(row=0, column=0, columnspan=2, pady=(
            0, padding_y), padx=padding_x, sticky=tk.W + tk.E)
        self.username_label.grid(
            row=1, column=0, sticky=tk.W, padx=padding_x, pady=padding_y)
        self.password_label.grid(
            row=2, column=0, sticky=tk.W, padx=padding_x, pady=padding_y)
        self.username_entry.grid(row=1, column=1, sticky=(
            tk.W, tk.E), padx=padding_x, pady=padding_y)
        self.password_entry.grid(row=2, column=1, sticky=(
            tk.W, tk.E), padx=padding_x, pady=padding_y)
        self.login_button.grid(
            row=3, column=1, padx=padding_x, pady=padding_y, sticky=tk.E)
        self.create_account_button.grid(
            row=4, column=1, padx=padding_x, pady=(padding_y, 0), sticky=tk.E)

    def create_registration_page(self):
        self.registration_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.welcome_label_registration = ttk.Label(
            self.registration_frame, text="Create Your Account", font=("Helvetica", 16))
        self.new_username_label = ttk.Label(
            self.registration_frame, text="New Username:")
        self.new_password_label = ttk.Label(
            self.registration_frame, text="New Password:")
        self.phone_label = ttk.Label(
            self.registration_frame, text="Phone Number:")
        self.address_label = ttk.Label(
            self.registration_frame, text="Address:")

        self.new_username_entry = ttk.Entry(self.registration_frame)
        self.new_password_entry = ttk.Entry(self.registration_frame, show="*")
        self.phone_entry = ttk.Entry(self.registration_frame)
        self.address_entry = ttk.Entry(self.registration_frame)

        self.register_button = ttk.Button(
            self.registration_frame, text="Register", command=self.register)
        self.back_to_login_button = ttk.Button(
            self.registration_frame, text="Back to Login", command=self.show_login_page)

        self.registration_frame.columnconfigure(1, weight=1)
        for i in range(7):
            self.registration_frame.rowconfigure(i, weight=1)

        padding_x = 40
        padding_y = 5

        self.welcome_label_registration.grid(
            row=0, column=0, columnspan=2, pady=10, padx=padding_x, sticky=tk.W + tk.E)
        self.new_username_label.grid(
            row=1, column=0, sticky=tk.W, padx=padding_x, pady=padding_y)
        self.new_password_label.grid(
            row=2, column=0, sticky=tk.W, padx=padding_x, pady=padding_y)
        self.phone_label.grid(
            row=3, column=0, sticky=tk.W, padx=padding_x, pady=padding_y)
        self.address_label.grid(
            row=4, column=0, sticky=tk.W, padx=padding_x, pady=padding_y)

        self.new_username_entry.grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=padding_x, pady=padding_y)
        self.new_password_entry.grid(
            row=2, column=1, sticky=(tk.W, tk.E), padx=padding_x, pady=padding_y)
        self.phone_entry.grid(
            row=3, column=1, sticky=(tk.W, tk.E), padx=padding_x, pady=padding_y)
        self.address_entry.grid(
            row=4, column=1, sticky=(tk.W, tk.E), padx=padding_x, pady=padding_y)

        self.register_button.grid(
            row=5, column=1, padx=padding_x, pady=padding_y, sticky=tk.E)
        self.back_to_login_button.grid(
            row=6, column=1, padx=padding_x, pady=(padding_y, 0), sticky=tk.E)

    def create_dropbox_page(self):
        self.dropbox_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.welcome_label_dropbox = ttk.Label(
            self.dropbox_frame, text="Welcome to Your File Storage", font=("Helvetica", 16))
        self.file_listbox = tk.Listbox(
            self.dropbox_frame, selectmode=tk.SINGLE, height=10, width=50)
        self.file_list_label = ttk.Label(
            self.dropbox_frame, text="Uploaded Files:", font=("Helvetica", 12))
        self.upload_button = ttk.Button(
            self.dropbox_frame, text="Upload File", command=self.upload_file)
        self.friend_list_button = ttk.Button(
            self.dropbox_frame, text="Friend List", command=self.show_friend_list_page)
        self.received_files_button = ttk.Button(
            self.dropbox_frame, text="Received Files", command=self.show_download_files_page)

        self.dropbox_frame.columnconfigure(0, weight=1)
        for i in range(7):
            self.dropbox_frame.rowconfigure(i, weight=1)

        padding_x = 20
        padding_y = 5

        self.welcome_label_dropbox.grid(
            row=0, column=0, columnspan=2, pady=10, padx=padding_x, sticky=tk.W + tk.E)
        self.file_list_label.grid(
            row=1, column=0, columnspan=2, pady=5, padx=padding_x, sticky=tk.W + tk.E)
        self.file_listbox.grid(
            row=2, column=0, columnspan=2, padx=padding_x, sticky=(tk.W, tk.E))
        self.upload_button.grid(
            row=4, column=0, columnspan=2, pady=padding_y, padx=padding_x, sticky=tk.E)
        self.friend_list_button.grid(
            row=5, column=0, columnspan=2, pady=padding_y, padx=padding_x, sticky=tk.E)
        self.received_files_button.grid(
            row=6, column=0, columnspan=2, pady=padding_y, padx=padding_x, sticky=tk.E)

    def add_friend(self):
        new_friend = self.new_friend_entry.get()
        if new_friend and new_friend not in self.friend_list:
            if self.current_user not in self.friend_list:
                self.friend_list[self.current_user] = []
            self.friend_list[self.current_user].append(new_friend)
            self.save_friend_list()
            self.populate_friend_listbox()
            self.new_friend_entry.delete(0, tk.END)
        else:
            error_label = ttk.Label(
                self.friend_list_frame, text="Invalid friend name", foreground="red")
            error_label.grid(row=4, column=1, columnspan=2, pady=5)
            self.friend_list_frame.after(2000, error_label.grid_forget)

    def create_friend_list_page(self):
        self.friend_list_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.welcome_label_friends = ttk.Label(
            self.friend_list_frame, text="Your Friend List", font=("Helvetica", 16))
        self.friend_listbox = tk.Listbox(
            self.friend_list_frame, selectmode=tk.SINGLE, height=10)
        self.new_friend_label = ttk.Label(
            self.friend_list_frame, text="New Friend:")
        self.new_friend_entry = ttk.Entry(self.friend_list_frame)
        self.add_friend_button = ttk.Button(
            self.friend_list_frame, text="Add Friend", command=self.add_friend)
        self.back_to_dropbox_button = ttk.Button(
            self.friend_list_frame, text="Back to Dropbox", command=self.show_dropbox_page)

        self.friend_list_frame.columnconfigure(0, weight=1)
        for i in range(6):
            self.friend_list_frame.rowconfigure(i, weight=1)

        padding_x = 20

        self.welcome_label_friends.grid(
            row=0, column=0, columnspan=2, pady=10, padx=padding_x, sticky=tk.W + tk.E)
        self.friend_listbox.grid(
            row=1, column=0, columnspan=2, pady=5, padx=padding_x, sticky=(tk.W, tk.E))
        self.new_friend_label.grid(
            row=2, column=0, sticky=tk.W, pady=5, padx=padding_x)
        self.new_friend_entry.grid(
            row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=padding_x)
        self.add_friend_button.grid(
            row=3, column=1, sticky=tk.E, pady=5, padx=padding_x)
        self.back_to_dropbox_button.grid(
            row=5, column=0, columnspan=2, pady=10, padx=padding_x, sticky=tk.W + tk.E)

    def create_download_files_page(self):
        self.download_files_frame.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.received_files_listbox = tk.Listbox(
            self.download_files_frame, selectmode=tk.SINGLE, height=10, width=50)
        self.received_files_label = ttk.Label(
            self.download_files_frame, text="Received Files:", font=("Helvetica", 12))
        self.download_button = ttk.Button(
            self.download_files_frame, text="Download Files", command=self.download_files)
        self.back_to_dropbox_button_download = ttk.Button(
            self.download_files_frame, text="Back to Dropbox", command=self.show_dropbox_page)

        self.download_files_frame.columnconfigure(0, weight=1)
        for i in range(6):
            self.download_files_frame.rowconfigure(i, weight=1)

        padding_x = 20

        self.received_files_label.grid(
            row=1, column=0, columnspan=2, pady=5, padx=padding_x, sticky=tk.W + tk.E)
        self.received_files_listbox.grid(
            row=2, column=0, columnspan=2, pady=5, padx=padding_x, sticky=(tk.W, tk.E))
        self.download_button.grid(
            row=4, column=0, columnspan=2, pady=5, padx=padding_x, sticky=tk.W + tk.E)
        self.back_to_dropbox_button_download.grid(
            row=5, column=0, columnspan=2, pady=10, padx=padding_x, sticky=tk.W + tk.E)

    def load_friend_list(self):
        try:
            with open("friend_list.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_login_info(self):
        with open("login_info.json", "w") as file:
            json.dump(self.login_info, file, indent=2)

    def save_friend_list(self):
        with open("friend_list.json", "w") as file:
            json.dump(self.friend_list, file, indent=2)

    def show_login_page(self):
        self.dropbox_frame.grid_remove()
        self.registration_frame.grid_remove()
        self.friend_list_frame.grid_remove()
        self.download_files_frame.grid_remove()
        self.login_frame.grid()

    def show_registration_page(self):
        self.login_frame.grid_remove()
        self.dropbox_frame.grid_remove()
        self.friend_list_frame.grid_remove()
        self.download_files_frame.grid_remove()
        self.registration_frame.grid()

    def show_dropbox_page(self):
        self.login_frame.grid_remove()
        self.registration_frame.grid_remove()
        self.friend_list_frame.grid_remove()
        self.download_files_frame.grid_remove()
        self.dropbox_frame.grid()
        self.populate_file_listbox()

    def show_friend_list_page(self):
        self.login_frame.grid_remove()
        self.registration_frame.grid_remove()
        self.dropbox_frame.grid_remove()
        self.friend_list_frame.grid()
        self.populate_friend_listbox()

    def show_download_files_page(self):
        self.login_frame.grid_remove()
        self.registration_frame.grid_remove()
        self.dropbox_frame.grid_remove()
        self.friend_list_frame.grid_remove()
        self.download_files_frame.grid()
        self.populate_received_files_listbox()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if the username exists and the password is correct
        if username in self.login_info and self.verify_password(password, self.login_info[username]):
            self.current_user = username
            if username not in self.friend_list:
                self.friend_list[username] = []
            self.show_dropbox_page()
        else:
            # For simplicity, just show an error message here
            error_label = ttk.Label(
                self.login_frame, text="Invalid username or password", foreground="red")
            error_label.grid(row=4, column=1, columnspan=2, pady=5)
            self.login_frame.after(2000, error_label.grid_forget)

    def verify_password(self, plain_password, stored_info):
        # For simplicity, let's use a basic hash function (sha256) for password verification
        hashed_input_password = hashlib.sha256(
            plain_password.encode()).hexdigest()

        # Print the hashed input password and stored hashed password for debugging
        print("Hashed Input Password:", hashed_input_password)
        print("Stored Hashed Password:", stored_info['password'])

        # Compare the hashed input password with the stored hashed password
        return hashed_input_password == stored_info['password']

    def register(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        phone_number = self.phone_entry.get()
        address = self.address_entry.get()

        if new_username in self.login_info:
            error_label = ttk.Label(
                self.registration_frame, text="Username already exists", foreground="red")
            error_label.grid(row=7, column=1, columnspan=2, pady=5)
            self.registration_frame.after(2000, error_label.grid_forget)
        else:
            # Hash the password and store the new account information
            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
            self.login_info[new_username] = {
                'password': hashed_password,
                'phone': phone_number,
                'address': address
            }
            self.save_login_info()
            self.show_login_page()

    def load_uploaded_files_list(self):
        try:
            with open("uploaded_files.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def upload_file(self):
        selected_friend = self.prompt_select_friend()
        file_path = filedialog.askopenfilename()

        if file_path and selected_friend:
            # update status to red (file is being sent)
            self.file_transfer_status_label.config(text="Sending file...", background="red")
            self.root.update()

            uploaded_file_info = {
                'friend': selected_friend,
                'file_name': os.path.basename(file_path)
            }

            if self.current_user not in self.uploaded_files:
                self.uploaded_files[self.current_user] = []
            self.uploaded_files[self.current_user].append(uploaded_file_info)
            self.save_uploaded_files()
            self.populate_file_listbox()

            # TODO: Upload the file to the FTP server to the selected friend

            # After the FTP upload logic
            # Update status to yellow (file is being transferred)
            #self.file_transfer_status_label.config(text="Transferring file...", background="yellow")
            #self.root.update()

            # Simulate the FTP transfer delay (replace with actual FTP transfer code)
            #import time
            #time.sleep(2)

            # Update status to green (file transfer complete)
            #self.file_transfer_status_label.config(text="File transferred successfully", background="green")

            # Clear the status after some time
            #self.root.after(5000, lambda: self.file_transfer_status_label.config(text="", background="white"))




        else:
            error_label = ttk.Label(
                self.dropbox_frame, text="No friend or file selected", foreground="red")
            error_label.grid(row=3, column=0, columnspan=2, pady=5)
            self.dropbox_frame.after(2000, error_label.grid_forget)

    def load_uploaded_files(self):
        try:
            with open("uploaded_files.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_uploaded_files(self):
        with open("uploaded_files.json", "w") as file:
            json.dump(self.uploaded_files, file, indent=2)

    def populate_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        if self.current_user not in self.uploaded_files:
            return
        for uploaded_file in self.uploaded_files[self.current_user]:
            friend = uploaded_file['friend']
            file_name = uploaded_file['file_name']
            self.file_listbox.insert(tk.END, f"{friend}: {file_name}")

    def prompt_select_friend(self):
        selected_friend_var = tk.StringVar()

        friend_combobox = ttk.Combobox(
            self.dropbox_frame, values=list(self.friend_list[self.current_user]), textvariable=selected_friend_var, state="readonly")
        friend_combobox.set("Select a Friend")
        friend_combobox.grid(row=3, column=0, columnspan=2, pady=5)

        self.dropbox_frame.wait_variable(selected_friend_var)

        selected_friend = selected_friend_var.get()

        friend_combobox.destroy()
        return selected_friend

    def download_files(self):
        # TODO: Download all files from the FTP server sent to the current user
        pass

    def populate_received_files_listbox(self):
        self.received_files_listbox.delete(0, tk.END)
        # TODO: Add logic to fetch received files and populate the listbox
        pass

    def populate_friend_listbox(self):
        self.friend_listbox.delete(0, tk.END)
        if self.current_user not in self.friend_list:
            return
        for friend in self.friend_list[self.current_user]:
            self.friend_listbox.insert(tk.END, friend)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
