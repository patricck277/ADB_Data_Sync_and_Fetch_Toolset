import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
import sys
from typing import Sequence, Type
import os
from datetime import datetime, timedelta
from colorama import Fore, init

DEVICE_ID = "5748202952"
REMOTE_PATH = "/sdcard/xxx/xxx"
LOCAL_BASE_PATH = "/home/pi/Downloads/xxx"
EXTENSION = ".xxx"
NEW_EXTENSION = ".xxx"


class ScriptArgs(Namespace):
    """Input arguments for type hinting of parsed arguments."""

    print_progress: bool


def parse_argv(args: Sequence[str]) -> Type[ScriptArgs]:
    """Define input arguments and return parser."""
    parser = ArgumentParser()
    parser.add_argument(
        "--print-progress", "-p", help="Print progress to stdout", action="store_true"
    )
    return parser.parse_args(args, namespace=ScriptArgs)


def check_device(device_id: str) -> bool:
    """Check if the specified device is connected and authorized."""
    result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
    print(f"ADB devices output:\n{result.stdout}")  # Debug: Output devices
    if device_id in result.stdout and "unauthorized" not in result.stdout:
        return True
    else:
        print(f"Device {device_id} is not connected or not authorized.")
        return False


def handle_download(
    device_id: str, remote_path: str, local_path: str, extension: str, target_date: str
) -> None:
    """
    Download files with the specified extension from the remote path on the device to the local path.
    """
    if check_device(device_id):
        # List all files with the specified extension
        list_files_command = f"adb -s {device_id} shell \"find {remote_path} -type f -name '*{extension}' -exec stat -c '%y %n' {{}} \\;\""
        result = subprocess.run(
            list_files_command, shell=True, capture_output=True, text=True
        )
        print(
            f"List files command output:\n{result.stdout}"
        )  # Debug: Output list of files
        if result.returncode == 0:
            files = result.stdout.splitlines()
            for file in files:
                # Extract date from file
                file_time_date = file[:file.index('/')-5]
                file_date = datetime.strptime(file_time_date, "%Y-%m-%d %H:%M:%S.%f").strftime("%Y%m%d")
                file_time = datetime.strptime(file_time_date, "%Y-%m-%d %H:%M:%S.%f").strftime("%H%M")
                # Extract filename from file
                filename = os.path.basename(file)
                print(
                    f"Checking file: {filename} with creation date: {file_date}"
                )  # Debug: Check each file's date
                if file_date == target_date:
                    # Split the filename by to recreate it with new values
                    splited_name = filename.split("_")
                    # Create the new filename with the new values
                    renamed_file = f"{splited_name[0]}_{splited_name[1]}_{splited_name[2]}_{file_date}_{file_time}_{splited_name[5].replace(EXTENSION, NEW_EXTENSION)}"
                    local_file_path = os.path.join(local_path, renamed_file)
                    # Fetch only path from the file
                    file_path = file[file.index('/'):]
                    # Download the file
                    download_command = f'adb -s {device_id} pull "{file_path}" "{local_file_path}"'
                    download_result = subprocess.run(download_command, shell=True, capture_output=True, text=True)
                    if download_result.returncode == 0:
                        print(f"Downloaded {file} to {local_file_path}")
                    else:
                        print(f"Failed to download {file}: {download_result.stderr}")
                else:
                    print(f"Skipped file: {filename} with date: {file_date}")  # Debug: Skipped file
        else:
            print(f"Failed to list files: {result.stderr}")
    else:
        print(f"Cannot proceed with download. Device {device_id} is not ready.")


def rename_files(local_path: str, old_extension: str, new_extension: str) -> None:
    """
    Rename files in the local path from old_extension to new_extension.
    """
    for file_path in Path(local_path).rglob(f"*{old_extension}"):
        new_file_path = file_path.with_suffix(new_extension)
        file_path.rename(new_file_path)
        print(f"Renamed {file_path} to {new_file_path}")

def rename_file(old_file: str, new_file: str) -> None:
    """
    Rename a file from old_extension to new_extension.
    """
    old_file.rename(new_file)
    print(f"Renamed {old_file} to {new_file}")

def main() -> None:
    """
    Main function that downloads receiver files based on the predefined arguments.
    """
    init()

    args = parse_argv(sys.argv[1:])
    print("---- DOWNLOAD-RXFILES started! Press CTRL+C to cancel. -----")
    print(f"Using device ID: {DEVICE_ID}")
    print(f"Remote path: {REMOTE_PATH}")
    print(f"Local base path: {LOCAL_BASE_PATH}")
    print(f"File extension: {EXTENSION}")

    if args.print_progress:
        os.environ["PRINT_PROGRESS"] = "1"

    # Calculate the target date (yesterday)
    target_date = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    formatted_target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"Target date (for filtering): {target_date}")  # Debug: Print target date
    print(
        f"Formatted target date (for folder): {formatted_target_date}"
    )  # Debug: Print formatted target date

    # Create a new directory with the formatted target date
    local_path = Path(LOCAL_BASE_PATH) / formatted_target_date
    local_path.mkdir(parents=True, exist_ok=True)

    handle_download(DEVICE_ID, REMOTE_PATH, str(local_path), EXTENSION, target_date)
    # rename_files(str(local_path), EXTENSION, NEW_EXTENSION)
    print("------------------ Script finished. Bye! -------------------")


if __name__ == "__main__":
    main()
