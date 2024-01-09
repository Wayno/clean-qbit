import os
import qbittorrentapi
import time
import shutil

# qBittorrent server information
qbt_host = 'http://localhost:9998/'  # Change this to your qBittorrent server URL with port 9998
qbt_username = 'admin'               # Change this to your qBittorrent username
qbt_password = 'password1'           # Change this to your qBittorrent password

# Directory path to check for folders
download_directory = 'D:/Completed/'  # Change to your desired directory
excluded_folders = ["sonarr-tv", "radarr"]

def get_active_qbittorrent_folders(qbt_client):
    # Retrieve the list of all torrents in qBittorrent
    torrents = qbt_client.torrents.info()

    # Extract the folder names from active torrents in qBittorrent
    active_folders = set()
    for torrent in torrents:
        torrent_name = os.path.basename(torrent.name)
        active_folders.add(torrent_name)

    return active_folders

def delete_folders_not_in_qbittorrent(active_folders, download_directory, qbt_client):
    for root, dirs, files in os.walk(download_directory, topdown=True):
        # Remove subfolders from the 'dirs' list to prevent traversal
        dirs[:] = [d for d in dirs if os.path.join(root, d) == os.path.join(download_directory, d)]

        for folder in dirs:
            folder_name = os.path.basename(folder)
            folder_path = os.path.join(root, folder)
            
            # Check if the folder is not part of an active qBittorrent torrent
            if folder_name not in active_folders and folder_name not in excluded_folders:
                print(f"Deleting folder: {folder_path}")
                shutil.rmtree(folder_path)

def is_folder_part_of_torrent(folder_name, qbt_client):
    # Retrieve the list of all torrents in qBittorrent
    torrents = qbt_client.torrents.info()
    
    # Extract the folder names from active torrents in qBittorrent
    active_folders = set()
    for torrent in torrents:
        torrent_name = os.path.basename(torrent.name)
        active_folders.add(torrent_name)
    
    # Check if the folder name is in the active_folders set
    return folder_name in active_folders

if __name__ == "__main__":
    try:
        cleanup_interval = 3600  # Cleanup every 3600 seconds (1 hour)
        qbt_client = qbittorrentapi.Client(host=qbt_host, username=qbt_username, password=qbt_password)
        qbt_client.auth_log_in()
        
        while True:
            print("Scanning downloads directory...")

            # Get the list of active folders in qBittorrent
            active_folders = get_active_qbittorrent_folders(qbt_client)

            print("Active folders in qBittorrent:")
            for folder in active_folders:
                print(folder)

            # Delete folders in the download directory not present in active qBittorrent torrents
            delete_folders_not_in_qbittorrent(active_folders, download_directory, qbt_client)

            print("Cleanup completed successfully.")

            # Countdown timer for the next cleanup
            for remaining_time in range(cleanup_interval, 0, -1):
                print(f"Next cleanup in {remaining_time} seconds", end="\r")
                time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
