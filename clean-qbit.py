import os
import qbittorrentapi
import time
import shutil
from colorama import Fore, Style, init
import threading
import signal
import sys
import msvcrt

# Initialize colorama
init(autoreset=True)

# Define color variables
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE
magenta = Fore.MAGENTA
cyan = Fore.CYAN
white = Fore.WHITE

# Set style for resetting color
reset_color = Style.RESET_ALL

# qBittorrent server information
qbt_host = 'http://localhost:9998/'  # Change this to your qBittorrent server URL with port 9998
qbt_username = 'admin'               # Change this to your qBittorrent username
qbt_password = 'password1'           # Change this to your qBittorrent password

# Directory path to check for folders
download_directory = 'D:/Completed/'  # Change to your desired directory
excluded_folders = ["sonarr-tv", "radarr"]

def get_active_qbittorrent_torrents(qbt_client):
    # Retrieve the list of all torrents in qBittorrent
    torrents = qbt_client.torrents.info()

    active_torrents = []
    for torrent in torrents:
        torrent_name = os.path.basename(torrent.name)
        active_torrents.append(torrent_name)

    return active_torrents

def delete_subdirectories_within_folder(folder_path, qbt_client):
    for subdirectory in os.listdir(folder_path):
        subdirectory_path = os.path.join(folder_path, subdirectory)
        if os.path.isdir(subdirectory_path) and not is_folder_part_of_torrent(subdirectory, qbt_client):
            try:
                shutil.rmtree(subdirectory_path)
                print(f"{red}Deleted subdirectory: {subdirectory_path}{reset_color}")
            except Exception as e:
                print(f"{yellow}Error deleting subdirectory: {subdirectory_path} - {e}{reset_color}")

def is_folder_part_of_torrent(folder_name, qbt_client):
    # Retrieve the list of all torrents in qBittorrent
    torrents = qbt_client.torrents.info()
    
    # Extract the torrent names from active torrents in qBittorrent
    active_torrents = []
    for torrent in torrents:
        torrent_name = os.path.basename(torrent.name)
        active_torrents.append(torrent_name)
    
    # Check if the folder name matches an active torrent name
    return folder_name in active_torrents

# Flag to indicate if the cleanup is in progress
cleanup_in_progress = False

def start_cleanup():
    global cleanup_in_progress
    try:
        qbt_client = qbittorrentapi.Client(host=qbt_host, username=qbt_username, password=qbt_password)
        qbt_client.auth_log_in()

        # Get the list of active torrents in qBittorrent
        active_torrents = get_active_qbittorrent_torrents(qbt_client)

        print("Active torrents in qBittorrent:")
        for torrent in active_torrents:
            print(torrent)

        # Rest of your cleanup code here...

        print(f"{green}Cleanup completed successfully.{reset_color}")
        cleanup_in_progress = False

    except Exception as e:
        print(f"An error occurred: {e}")
        cleanup_in_progress = False
        
def display_countdown_timer(timer_duration):
    cleanup_in_progress = False  # Flag to track cleanup state
    for remaining_time in range(timer_duration, 0, -1):
        sys.stdout.write(f"\rNext cleanup in {red}{remaining_time} seconds{reset_color}")
        sys.stdout.flush()
        if msvcrt.kbhit() and msvcrt.getch() == b'\r':
            if not cleanup_in_progress:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Starting cleanup...")
                cleanup_in_progress = True
                start_cleanup()
                cleanup_in_progress = False
                time.sleep(2)  # Sleep to prevent accidental re-triggering
        time.sleep(1)
    sys.stdout.write("\r" + " " * 40 + "\r")  # Clear countdown timer line
    sys.stdout.flush()

def exit_handler(sig, frame):
    global cleanup_in_progress
    if cleanup_in_progress:
        print("\nCleanup is in progress. Please wait for it to complete.")
    else:
        print("\nExiting the script.")
        os._exit(0)

if __name__ == "__main__":
    try:
        cleanup_interval = 3600  # Cleanup every 3600 seconds (1 hour)
        qbt_client = qbittorrentapi.Client(host=qbt_host, username=qbt_username, password=qbt_password)
        qbt_client.auth_log_in()

        # Set up Ctrl+C signal handler
        signal.signal(signal.SIGINT, exit_handler)

        print("Starting script...")
        print("Press Enter at any point to run cleanup.")

        while True:
            display_countdown_timer(cleanup_interval)  # Start countdown

            # Check if Enter is pressed to start cleanup
            if msvcrt.kbhit() and msvcrt.getch() == b'\r':
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Starting cleanup...")
                cleanup_in_progress = True
                start_cleanup()
                cleanup_in_progress = False
                time.sleep(2)  # Sleep to prevent accidental re-triggering

    except Exception as e:
        print(f"An error occurred: {e}")
