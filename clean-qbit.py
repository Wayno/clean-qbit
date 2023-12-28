import os
import qbittorrentapi
import time
import shutil

# qBittorrent server information
qbt_host = 'http://localhost:9998/'  # Change this to your qBittorrent server URL with port 9998
qbt_username = 'admin'               # Change this to your qBittorrent username
qbt_password = 'password1'           # Change this to your qBittorrent password

# Directory path to check for folders
download_directory = 'D:/Completed/sonarr-tv'  # Change to your desired directory

def get_active_qbittorrent_folders():
    qbt_client = qbittorrentapi.Client(host=qbt_host, username=qbt_username, password=qbt_password)

    # Retrieve the list of all torrents in qBittorrent
    torrents = qbt_client.torrents.info()

    # Extract the folder names from active torrents in qBittorrent
    active_folders = set()
    for torrent in torrents:
        torrent_name = os.path.basename(torrent.name)
        active_folders.add(torrent_name)

    return active_folders

def delete_folders_not_in_qbittorrent(active_folders, download_directory):
    for root, dirs, files in os.walk(download_directory, topdown=False):
        for folder in dirs:
            folder_name = os.path.basename(folder)
            # Check if the folder name is not in the active_folders set
            if folder_name not in active_folders:
                folder_path = os.path.join(root, folder)
                print(f"Deleting folder: {folder_path}")
                shutil.rmtree(folder_path)

if __name__ == "__main__":
    try:
        while True:
            print("Scanning downloads directory...")

            # Get the list of active folders in qBittorrent
            active_folders = get_active_qbittorrent_folders()

            print("Active folders in qBittorrent:")
            for folder in active_folders:
                print(folder)

            # Delete folders in the download directory not present in active qBittorrent torrents
            delete_folders_not_in_qbittorrent(active_folders, download_directory)

            print("Cleanup completed successfully.")

            # Sleep for 60 minutes (3600 seconds) before the next iteration
            time.sleep(3600)
    except Exception as e:
        print(f"An error occurred: {e}")
