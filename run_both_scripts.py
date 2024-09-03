import subprocess

def run_fetch_data():
    """Run the fetch_data.py script."""
    result = subprocess.run(['python3', '/home/pi/fetch_data.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("fetch_data.py completed successfully.")
    else:
        print(f"fetch_data.py failed: {result.stderr}")

def run_sync_script():
    """Run the sync_script.py script."""
    result = subprocess.run(['python3', '/home/pi/sync_script.py'], capture_output=True, text=True)
    if result.returncode == 0:
        print("sync_script.py completed successfully.")
    else:
        print(f"sync_script.py failed: {result.stderr}")

def main():
    run_fetch_data()
    run_sync_script()

if __name__ == "__main__":
    main()
