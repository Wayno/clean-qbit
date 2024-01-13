import os
import qbittorrentapi
import time
import shutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define color variables
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE

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

if __name__ == "__main__":
    try:
        cleanup_interval = 3600  # Cleanup every 3600 seconds (1 hour)
        qbt_client = qbittorrentapi.Client(host=qbt_host, username=qbt_username, password=qbt_password)
        qbt_client.auth_log_in()

        while True:
            # Clear the screen (based on the operating system)
            os.system('cls' if os.name == 'nt' else 'clear')

            print(f"{blue}Scanning downloads directory...{reset_color}")

            # Get the list of active torrents in qBittorrent
            active_torrents = get_active_qbittorrent_torrents(qbt_client)

            print("Active torrents in qBittorrent:")
            for torrent in active_torrents:
                print(torrent)

            # Delete subdirectories within 'sonarr-tv' and 'radarr'
            for excluded_folder in excluded_folders:
                excluded_folder_path = os.path.join(download_directory, excluded_folder)
                if os.path.exists(excluded_folder_path):
                    delete_subdirectories_within_folder(excluded_folder_path, qbt_client)

            print(f"{green}Cleanup completed successfully.{reset_color}")

            # Countdown timer for the next cleanup
            for remaining_time in range(cleanup_interval, 0, -1):
                print(f"Next cleanup in {red}{remaining_time} seconds{reset_color}", end="\r")
                time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
