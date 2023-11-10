import os
from ftplib import FTP
import json

# Function to create a new user account
def createAccount():
    username = input('Please enter a new username: ')
    if username in users:
        print("Username already exists. Try a different username.")
        return
    password = input('Please enter a password: ')
    users[username] = password
    saveUsersToJson()
    print('Account created successfully.')

# Function to list all users
def listUsers():
    print("List of all users:")
    for username in users:
        print(username)

# Function to save user data to a JSON file
def saveUsersToJson():
    with open('users.json', 'w') as user_file:
        json.dump(users, user_file)

# Function to load user data from a JSON file
def loadUsersFromJson():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as user_file:
            return json.load(user_file)
    return {}

print("Welcome to DataMule Data Depot!")
users = loadUsersFromJson()

while True:
    print("Please Enter Username (or 'create' to create a new account, or 'exit' to quit):")
    username = input()
    
    if username == 'create':
        createAccount()
    elif username == 'exit':
        print("Goodbye!")
        break
    elif username in users:
        password = input("Please Enter Password: ")
        if users[username] == password:
            print("Select which Village you are in: A, B, C, D")
            village = input()
            if village == 'A':
                ftp_server = '10.226.118.180'
                network_name = 'eduroam'
                ftp_username = 'ftp-villageA'
                ftp_password = '1234'

                ftp = FTP()
                # Connect to the FTP server
                ftp.connect(ftp_server)
                # Log in with the provided credentials
                ftp.login(ftp_username, ftp_password)
                print("Would you like to upload or download files: 'U' or 'D', or would you like to find other users 'list'?")
                upload_or_download = input()

                if upload_or_download == 'U':
                    # Ask the user for the file to upload
                    local_file_path = input("Enter the path to the file you want to upload (Make sure the file you upload contains the username of the user you would like to receive the file): ")
                    if os.path.isfile(local_file_path):
                        # Get the file name from the local path
                        file_name = os.path.basename(local_file_path)
                        # Upload the file to the FTP server
                        with open(local_file_path, 'rb') as local_file:
                            ftp.storbinary(f'STOR {file_name}', local_file)
                        print(f'Uploaded {file_name} to the FTP server')
                    else:
                        print("File not found. Upload canceled.")
                elif upload_or_download == 'D':
                    local_directory_download = input("Please select the directory you would like to download the files to: ")
                    # List files and directories in the current directory on the FTP server
                    file_list = ftp.nlst()
                    if not os.path.exists(local_directory_download):
                        os.makedirs(local_directory_download)
                    user_files = [remote_filename for remote_filename in file_list if username in remote_filename]
                    for remote_filename in user_files:
                        local_filepath = os.path.join(local_directory_download, remote_filename)
                        with open(local_filepath, 'wb') as local_file:
                            ftp.retrbinary(f'RETR {remote_filename}', local_file.write)
                        print(f'Downloaded {remote_filename} to {local_filepath}')
                elif upload_or_download == 'list':
                    listUsers()
                
                else:
                    print("Invalid option. Please choose 'U' for upload or 'D' for download.")
                # Close the FTP connection
                ftp.quit()
            else:
                print("Invalid village. Please select A, B, C, or D.")
        else:
            print("Invalid password. Please try again.")
    else:
        print("Username not found. Please try again.")