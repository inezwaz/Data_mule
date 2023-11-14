import os
import re

#statuscript
def get_file_statuses(log_file_path, directory_path):
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

# Example usage
log_file_path = r'C:\Users\newti\Desktop\FTPfolder\client.log'
directory_path = r'C:\Users\newti\Desktop\FTPfolder'

status_dict = get_file_statuses(log_file_path, directory_path)
for filename, status in status_dict.items():
    print(f"{filename}: {status}")
