import requests
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def download_range(url, destination, start_byte, end_byte, progress_bar):
    """Download a specific range of bytes from the given URL and save it to the specified destination."""
    try:
        headers = {'Range': f'bytes={start_byte}-{end_byte}'}
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        with open(destination, 'ab') as file:
            for data in response.iter_content(1024):
                file.write(data)
                progress_bar.update(len(data))

        progress_bar.close()
        print(f"\nRange download successful for bytes {start_byte}-{end_byte}.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading range: {e}")

def download_file_with_progress(url, destination, num_connections=1):
    """Download a file from the given URL and save it to the specified destination with multiple connections."""
    try:
        response = requests.head(url)
        total_size = int(response.headers.get('content-length', 0))

        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc=f'Downloading {os.path.basename(destination)}', ncols=80)

        ranges = [(i * (total_size // num_connections), ((i + 1) * (total_size // num_connections)) - 1) for i in range(num_connections)]

        with ThreadPoolExecutor(max_workers=num_connections) as executor:
            futures = []
            for start_byte, end_byte in ranges:
                futures.append(executor.submit(download_range, url, destination, start_byte, end_byte, progress_bar))

            # Wait for all threads to finish
            for future in futures:
                future.result()

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

def download_multiple_files(urls, destination_folder=".", num_connections=1):
    """Download multiple files concurrently."""
    for url in urls:
        filename = url.split("/")[-1]
        destination = os.path.join(destination_folder, filename)
        download_file_with_progress(url, destination, num_connections=num_connections)

def validate_file_type(url, allowed_file_types):
    """Check if the file type is allowed for download."""
    filename = url.split("/")[-1]
    file_extension = os.path.splitext(filename)[1][1:]  # Remove the leading dot

    if not file_extension.lower() in allowed_file_types:
        print(f"Warning: File type '{file_extension}' not allowed for download from {url}.")
        return False
    return True

def main():
    print("=== PyDownloader with Progress Bar, Resumable Download, Multiple File Downloads, File Type Validation, and Multiple Connections ===")
    
    # Get multiple URLs from the user
    urls = input("Enter multiple URLs separated by spaces: ").split()

    # Choose destination folder
    destination_folder = input("Enter the destination folder (or press Enter to save in the current directory): ") or "."

    # Choose the number of connections
    num_connections = int(input("Enter the number of connections to use for each download: ") or "1")

    # Validate and download files
    allowed_file_types = ["jpg", "jpeg", "png", "gif", "txt", "pdf"]  # Example allowed file types
    for url in urls:
        if validate_file_type(url, allowed_file_types):
            download_multiple_files([url], destination_folder, num_connections)

if __name__ == "__main__":
    main()
