import os
import qbittorrentapi
import time
import shutil

# qBittorrent server information
qbt_host = 'http://localhost:8080/'  # Change this to your qBittorrent server URL with port 9998
qbt_username = 'admin'               # Change this to your qBittorrent username
qbt_password = 'password'           # Change this to your qBittorrent password

# Directory path to check for files/folders
download_directory = 'D:/Completed/sonarr-tv'  # Change to your desired directory

def get_qbittorrent_downloads():
    qbt_client = qbittorrentapi.Client(host=qbt_host, username=qbt_username, password=qbt_password)

    # Retrieve the list of all torrents in qBittorrent
    torrents = qbt_client.torrents.info()

    # Extract the file paths from the torrent list
    torrent_files = set()
    for torrent in torrents:
        for file in torrent.files:
            torrent_files.add(file.name)  # Add the file path to the set

    return torrent_files

def delete_files_and_folders_not_in_qbittorrent(torrent_files, download_directory):
    for root, dirs, files in os.walk(download_directory, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            # Check if the file path is not in the torrent_files set
            if file_path not in torrent_files:
                print(f"Deleting file: {file_path}")
                os.remove(file_path)
        
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            # Check if the folder path is not in the torrent_files set
            if folder_path not in torrent_files:
                print(f"Deleting folder: {folder_path}")
                shutil.rmtree(folder_path)

if __name__ == "__main__":
    try:
        while True:
            print("Scanning downloads directory...")
            
            # Get the list of files in qBittorrent
            torrent_files = get_qbittorrent_downloads()

            print("Files found in qBittorrent:")
            for file in torrent_files:
                print(file)

            # Delete files and folders in the download directory not present in qBittorrent
            delete_files_and_folders_not_in_qbittorrent(torrent_files, download_directory)

            print("Cleanup completed successfully.")

            # Sleep for 60 minutes (3600 seconds) before the next iteration
            time.sleep(3600)
    except Exception as e:
        print(f"An error occurred: {e}")
