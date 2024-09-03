import os
import subprocess
from datetime import datetime

# Directory paths
local_base_directory = "/home/pi/Downloads/xxx"
remote_base_directory = "/mnt/xxx_data"

# Function to mount the remote directory
def mount_remote_directory():
    # Check if the directory is already mounted
    unmount_remote_directory()

    credentials_file = "/home/pi/.smbcredentials"
    mount_command = f"sudo mount -t cifs //xx.xx.xx.xx/xxx/xxx/xxx/xxx {remote_base_directory} -o credentials={credentials_file},uid=pi,gid=pi,sec=ntlmssp,vers=3.0"
    subprocess.run(mount_command, shell=True, check=True)

# Function to unmount the remote directory
def unmount_remote_directory():
    unmount_command = f"sudo umount {remote_base_directory}"
    subprocess.run(unmount_command, shell=True)

# Function to find the latest dated folder
def get_latest_folder(base_directory):
    all_folders = [os.path.join(base_directory, d) for d in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, d))]
    latest_folder = max(all_folders, key=os.path.getmtime)
    return latest_folder

# Function to sync files
def sync_files(local_directory, remote_directory):
    rsync_command = f"rsync -av {local_directory}/ {remote_directory}/"
    subprocess.run(rsync_command, shell=True, check=True)

# Main script function
def main():
    try:
        # Mount the remote directory
        mount_remote_directory()

        # Find the latest dated folder
        latest_local_folder = get_latest_folder(local_base_directory)
        date_folder_name = os.path.basename(latest_local_folder)
        # remote_directory = os.path.join(remote_base_directory, date_folder_name)

        # Create dated folder on the server
        # os.makedirs(remote_directory, exist_ok=True)

        # Sync files
        sync_files(latest_local_folder, remote_base_directory)
    finally:
        # Unmount the remote directory
        unmount_remote_directory()

if __name__ == "__main__":
    main()
