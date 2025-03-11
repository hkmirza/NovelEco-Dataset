import os
import time
import requests
import yt_dlp
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# File containing Facebook URLs
input_file = "facebook_urls.txt"
output_folder = "facebook_downloads"
os.makedirs(output_folder, exist_ok=True)

# Setup Selenium WebDriver
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Read Facebook URLs from file and start from line 898
with open(input_file, "r") as file:
    urls = [line.strip() for line in file]

# Ensure we start from line 898
urls = urls[897:]  # Python uses zero-based indexing, so line 898 is index 897

# Function to extract images, videos, and metadata
def extract_facebook_data(fb_url):
    try:
        driver.get(fb_url)
        time.sleep(5)  # Allow page to load

        # Extract metadata
        soup = BeautifulSoup(driver.page_source, "html.parser")
        username = soup.find("span", class_="nc684nl6").text if soup.find("span", class_="nc684nl6") else "Unknown User"
        post_date = soup.find("abbr").text if soup.find("abbr") else "Unknown Date"
        caption = soup.find("div", class_="kvgmc6g5").text if soup.find("div", class_="kvgmc6g5") else "No Caption"

        # Extract comments
        comments_section = soup.find_all("div", class_="cwj9ozl2")
        comments_text = "\n".join([comment.text for comment in comments_section]) if comments_section else "No comments"

        # Extract image URLs
        img_urls = [img["src"] for img in soup.find_all("img") if "scontent" in img["src"]]

        return img_urls, username, post_date, caption, comments_text

    except Exception as e:
        print(f"⚠️ Failed to extract data from {fb_url}: {e}")
        return None, None, None, None, None

# Function to download videos using yt-dlp
def download_facebook_video(video_url, output_path):
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'bestvideo+bestaudio/best',
        'quiet': True,
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print(f"✅ Downloaded video: {output_path}")
    except Exception as e:
        print(f"❌ Error downloading video from {video_url}: {e}")

# Process each URL from line 898 and save images, videos, and text files in sequence
file_count = 898  # Start numbering from 898

for url in urls:
    if not url:
        print(f"⚠️ Skipping empty line {file_count}")
        file_count += 1
        continue

    img_urls, username, post_date, caption, comments = extract_facebook_data(url)

    # Try to download video first
    video_path = os.path.join(output_folder, f"number{file_count}.mp4")
    download_facebook_video(url, video_path)

    # Check if the video exists after download
    if os.path.exists(video_path):
        file_count += 1  # Increment numbering
    elif not img_urls:
        print(f"❌ No media found for {url}, skipping...")
        continue  # Skip if no media is found

    # Download images
    for img_url in img_urls:
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                img_path = os.path.join(output_folder, f"number{file_count}.jpg")
                with open(img_path, "wb") as img_file:
                    for chunk in response.iter_content(1024):
                        img_file.write(chunk)
                print(f"✅ Downloaded image: {img_path}")
        except Exception as e:
            print(f"❌ Error downloading image from {url}: {e}")

    # Save metadata to text file
    text_file_path = os.path.join(output_folder, f"number{file_count}.txt")
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(
            f"📌 Username: {username}\n"
            f"🗓️ Date: {post_date}\n"
            f"📝 Title: Facebook Post\n\n"
            f"📝 Caption:\n{caption}\n\n"
            f"💬 Comments:\n{comments}"
        )

    print(f"📝 Saved metadata as number{file_count}.txt")

    file_count += 1  # Increment numbering for the next entry

# Close browser session
driver.quit()

print("🎉 Download completed! Check the 'facebook_downloads' folder.")
