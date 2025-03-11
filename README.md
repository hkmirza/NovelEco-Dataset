# README: Social Media Data Scraping (Instagram, Facebook, Flickr)

## Table of Contents
1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation Guide](#installation-guide)
4. [Setting Up API Keys](#setting-up-api-keys)
5. [Running the Scrapers](#running-the-scrapers)
6. [Troubleshooting](#troubleshooting)
7. [License](#license)

## Introduction
This project scrapes data from Instagram, Facebook, and Flickr using APIs and web scraping techniques. The collected data is intended for sentiment analysis and research purposes.

## Prerequisites
- Windows, macOS, or Linux
- Python 3.8+
- Basic knowledge of Python and REST APIs

## Installation Guide

### Step 1: Install Python
If you don't have Python installed, download and install it from:
- [Python Official Website](https://www.python.org/downloads/)

Verify installation:
```sh
python --version
```

### Step 2: Create a Virtual Environment
To avoid dependency conflicts, create a virtual environment:
```sh
python -m venv scraping_env
source scraping_env/bin/activate  # macOS/Linux
scraping_env\Scripts\activate  # Windows
```

### Step 3: Install Required Libraries
Run the following command to install all required Python packages:
```sh
pip install requests beautifulsoup4 selenium instaloader facebook-sdk flickrapi pandas
```

#### Library Breakdown:
- `requests`: For handling HTTP requests
- `beautifulsoup4`: For parsing HTML data (if needed for scraping)
- `selenium`: For browser automation (Instagram scraping workaround)
- `instaloader`: For downloading Instagram posts
- `facebook-sdk`: Facebook Graph API
- `flickrapi`: For accessing Flickr API
- `pandas`: For data processing and saving scraped data

## Setting Up API Keys

### Instagram
- Use `Instaloader` to download posts and captions without an API key.
- Install Instaloader:
  ```sh
  pip install instaloader
  ```
- Login:
  ```sh
  instaloader --login your_username
  ```
- Scrape user posts:
  ```sh
  instaloader profile target_username
  ```

### Facebook
- Create a Facebook Developer account at [Facebook Developers](https://developers.facebook.com/)
- Create an App and get an access token.
- Store the token in an environment variable or use it directly in the script.

### Flickr
- Register for a Flickr API key at [Flickr API](https://www.flickr.com/services/api/)
- Use `flickrapi` to authenticate:
  ```python
  import flickrapi
  api_key = "your_api_key"
  flickr = flickrapi.FlickrAPI(api_key, format='parsed-json')
  ```

## Running the Scrapers

### Instagram
Run the following command to scrape posts:
```sh
python instagram_scraper.py
```

### Facebook
Run the script to fetch posts using the Graph API:
```sh
python facebook_scraper.py
```

### Flickr
Run the Flickr script to fetch images and metadata:
```sh
python flickr_scraper.py
```

## Troubleshooting
- **Issue:** `ModuleNotFoundError`
  - **Solution:** Ensure the virtual environment is activated and run `pip install -r requirements.txt`.
- **Issue:** `403 Forbidden` error on API requests
  - **Solution:** Ensure your API keys and tokens are correct and valid.
- **Issue:** Instagram login issues with `instaloader`
  - **Solution:** Enable two-factor authentication and use an App Password.

## License
This project is intended for educational and research purposes. Please ensure compliance with the terms of service of Instagram, Facebook, and Flickr when scraping data.

