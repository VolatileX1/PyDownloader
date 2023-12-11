import requests
import os
from tqdm import tqdm

def download_file_with_progress(url, destination):
    """Download a file from the given URL and save it to the specified destination with a progress bar."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 KB
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', ncols=80)

        with open(destination, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()

        print(f"\nDownload successful. File saved at: {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

def main():
    print("=== PyDownloader with Progress Bar ===")
    url = input("Enter the URL of the file to download: ")
    
    # Extracting the filename from the URL
    filename = url.split("/")[-1]
    
    destination = input(f"Enter the destination path to save '{filename}' (or press Enter to save in the current directory): ")
    
    if not destination:
        destination = filename
    elif os.path.isdir(destination):
        destination = os.path.join(destination, filename)
    
    download_file_with_progress(url, destination)

if __name__ == "__main__":
    main()
