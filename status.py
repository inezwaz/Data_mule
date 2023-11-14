#import re
#file_statuses = {}


#def get_status(line):
    #if "download" in line:
        #return "In Transit (Yellow)"
    #elif "upload" in line:
        #return "Delivered (Green)"
    #else:
        #return "Other (Gray)"


#def update_file_status(filename, status):
    #file_statuses[filename] = status


#log_file_path = r'C:\Users\newti\Desktop\FTPfolder\client.log'


##Open the log file in read mode
#with open(log_file_path, 'r') as log_file:
    # Define regular expressions for download and upload entries
    #download_pattern = re.compile(r"download (.+?) to")
    #upload_pattern = re.compile(r"upload (.+?) to")

    # Read the file line by line
    #for line in log_file:
        # Skip lines related to .log files
        #if ".log" in line:
            #continue

        # Get the status based on the line content
        #status = get_status(line)

        # Extract filename using regular expressions
        #download_match = download_pattern.search(line)
        #upload_match = upload_pattern.search(line)

        #if download_match:
            #filename = download_match.group(1)
        #elif upload_match:
            #filename = upload_match.group(1)
        #else:
            #continue  # Skip lines that are not download or upload actions

        # Update the file status
        #update_file_status(filename, status)

        # Process each line and print the status
        #print(
            #f"Status: {status}, Filename: {filename}, Log Entry: {line.strip()}")

##Print the final file statuses
#print("\nFinal File Statuses:")
#for filename, status in file_statuses.items():
    #print(f"{filename}: {status}")
