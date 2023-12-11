import requests
import os

def download_file(url, destination):
    """Download a file from the given URL and save it to the specified destination."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses (4xx and 5xx)
        
        with open(destination, 'wb') as file:
            file.write(response.content)
        
        print(f"Download successful. File saved at: {destination}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

def main():
    print("=== PyDownloader ===")
    url = input("Enter the URL of the file to download: ")
    
    # Extracting the filename from the URL
    filename = url.split("/")[-1]
    
    destination = input(f"Enter the destination path to save '{filename}' (or press Enter to save in the current directory): ")
    
    if not destination:
        destination = filename
    elif os.path.isdir(destination):
        destination = os.path.join(destination, filename)
    
    download_file(url, destination)

if __name__ == "__main__":
    main()
