# PyDownloader

PyDownloader is a Python script that provides a simple and versatile command-line download manager. It supports various features such as progress bars, resumable downloads, multiple file downloads, file type validation, and breaking a file into multiple connections for faster downloads.

## Features

- **Progress Bar:** Visualize the download progress with a dynamic progress bar.
- **Resumable Downloads:** Resume interrupted downloads using the `Range` header.
- **Multiple File Downloads:** Download multiple files sequentially.
- **File Type Validation:** Check file types before downloading and provide warnings.
- **Configurable Settings:** Allow users to customize download behavior, set default download directories, and configure the number of concurrent downloads.

## Requirements

- Python 3.6 or later
- `requests` library
- `tqdm` library

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/VolatileX1/PyDownloader.git
   cd PyDownloader

2. Install dependencies:

   ```bash
   pip install -r requirements.txt

## Usage

1. Run the script:

   ```bash
   python pydownloader.py

2. Follow the prompts to enter URLs and set download options

## Configuration

- Modify the allowed_file_types list in the script to customize the allowed file types.
- Change the num_connections variable in the script to adjust the number of connections for faster downloads.

