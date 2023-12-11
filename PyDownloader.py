import requests
import os
from tqdm import tqdm

def download_file_with_progress(url, destination):
    """Download a file from the given URL and save it to the specified destination with a progress bar."""
    try:
        if os.path.exists(destination):
            resume_header = {'Range': 'bytes=%d-' % os.path.getsize(destination)}
        else:
            resume_header = {}

        response = requests.get(url, headers=resume_header, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0)) + os.path.getsize(destination)
        block_size = 1024  # 1 KB
        progress_bar = tqdm(total=total_size, initial=os.path.getsize(destination), unit='B', unit_scale=True, desc=f'Downloading {os.path.basename(destination)}', ncols=80)

        with open(destination, 'ab') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()

        print(f"\nDownload successful. File saved at: {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

def download_multiple_files(urls, destination_folder="."):
    """Download multiple files sequentially."""
    for url in urls:
        filename = url.split("/")[-1]
        destination = os.path.join(destination_folder, filename)
        download_file_with_progress(url, destination)

def validate_file_type(url, allowed_file_types):
    """Check if the file type is allowed for download."""
    filename = url.split("/")[-1]
    file_extension = os.path.splitext(filename)[1][1:]  # Remove the leading dot

    if not file_extension.lower() in allowed_file_types:
        print(f"Warning: File type '{file_extension}' not allowed for download from {url}.")
        return False
    return True

def main():
    print("=== PyDownloader with Progress Bar, Resumable Download, Multiple File Downloads, and File Type Validation ===")
    
    # Get multiple URLs from the user
    urls = input("Enter multiple URLs separated by spaces: ").split()

    # Choose destination folder
    destination_folder = input("Enter the destination folder (or press Enter to save in the current directory): ") or "."

    # Validate and download files
    allowed_file_types = ["jpg", "jpeg", "png", "gif", "txt", "pdf"]  # Example allowed file types
    for url in urls:
        if validate_file_type(url, allowed_file_types):
            download_multiple_files([url], destination_folder)

if __name__ == "__main__":
    main()
