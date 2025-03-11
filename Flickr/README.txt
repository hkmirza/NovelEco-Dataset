# Flickr Image Downloader

This script downloads images from Flickr URLs and saves metadata (username, title, caption, hashtags, and comments) in text files. It works without requiring a Flickr API key.

---

## Requirements

Make sure you have **Python 3.x** installed. You will also need the following Python packages:

- `requests`
- `beautifulsoup4`

---

## Installation

### 1. Install Python (If Not Installed)
- Download and install Python from: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Make sure Python and pip are added to your system PATH.

### 2. Install Required Packages
Open **Command Prompt (`cmd`)** or **Anaconda Prompt** and run:

```
pip install requests beautifulsoup4
```

---

## Setup

### 1. Prepare Your Flickr URLs File
- Create a text file named `flickr_urls.txt`
- Add **one Flickr photo URL per line**, for example:
  
  ```
  https://www.flickr.com/photos/c_morosus/52429673418
  https://www.flickr.com/photos/eaviles/15418313141
  https://www.flickr.com/photos/fromsleepyhollowroad/7464947004
  ```

### 2. Download the Python Script
Save the script as `flickr_downloader.py` in the same directory as `flickr_urls.txt`.

---

## Running the Script

### Windows
1. Navigate to the script folder in Command Prompt:
   ```
   cd "C:\Users\YourUsername\Path\To\Your\Folder"
   ```
   *(Replace with the actual path where the script is saved.)*

2. Run the script:
   ```
   python flickr_downloader.py
   ```

### Mac/Linux
1. Open Terminal and go to the script folder:
   ```
   cd /path/to/your/folder
   ```

2. Run the script:
   ```
   python3 flickr_downloader.py
   ```

---

## Output

The script downloads images and saves metadata in a folder called `flickr_downloads/`.

### Example Output
```
flickr_downloads/
├── number1.jpg   # Image from line 1
├── number1.txt   # Metadata from line 1
├── number2.jpg   # Image from line 2
├── number2.txt   # Metadata from line 2
(Skips missing line)
├── number4.jpg   # Image from line 4
├── number4.txt   # Metadata from line 4
```

### Example `number1.txt`
```
Username: ThomasWilson
Date: 2021-09-17 14:05:08
Title: Urban Wildlife Hide

Caption:
A hide overlooking grasslands at the edge of a flood prevention area.

Hashtags: #urbanwildlifewatching #naturephotography

Comments:
user1: Amazing shot!
user2: Love the details!
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'requests'`
**Fix:** Install missing packages:
```
pip install requests beautifulsoup4
```

### `SSLError: Can't connect to HTTPS URL`
**Fix:** Update Python's SSL certificates:
```
pip install --upgrade certifi urllib3 requests
```

### `No Image Found for URL`
**Fix:** Ensure the Flickr URL is valid and accessible.

---

## Features
- Extracts and downloads images from Flickr photo URLs
- Saves images sequentially (`number1.jpg`, `number2.jpg`, etc.)
- Extracts and saves metadata (`username`, `title`, `caption`, `hashtags`, `comments`)
- Skips missing images and continues downloading
- No API key required!

---



