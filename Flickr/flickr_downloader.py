import requests
import os
import time
from bs4 import BeautifulSoup

# File containing Flickr URLs
input_file = "flickr_urls.txt"
output_folder = "flickr_downloads"
os.makedirs(output_folder, exist_ok=True)

# Read Flickr URLs from the file
with open(input_file, "r") as file:
    urls = [line.strip() for line in file]

# Function to extract image URL and metadata
def extract_flickr_data(flickr_url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(flickr_url, headers=headers)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch page for {flickr_url}")
            return None, None, None, None, None, None, None

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract image URL
        img_tag = soup.find("meta", property="og:image")
        img_url = img_tag["content"] if img_tag else None

        # Extract metadata
        username = soup.find("a", class_="owner-name")  # Username
        username = username.text.strip() if username else "Unknown User"

        title = soup.find("title")  # Image Title
        title = title.text.strip() if title else "No Title"

        date_taken = soup.find("span", class_="date-taken-label")  # Date
        date_taken = date_taken.text.strip() if date_taken else "Unknown Date"

        description = soup.find("meta", {"property": "og:description"})  # Caption
        description = description["content"].strip() if description else "No Caption"

        tags = soup.find_all("a", class_="Pill")  # Hashtags
        hashtags = " ".join([tag.text for tag in tags if "#" in tag.text]) if tags else "No Hashtags"

        # Extract Comments
        comments_text = "No comments"
        comments_section = soup.find("div", class_="comments-list")
        if comments_section:
            comment_items = comments_section.find_all("p", class_="comment-content")
            comments_text = "\n".join([f"{comment.text.strip()}" for comment in comment_items])

        return img_url, username, title, date_taken, description, hashtags, comments_text

    except Exception as e:
        print(f"⚠️ Failed to extract data from {flickr_url}: {e}")
        return None, None, None, None, None, None, None

# Process each URL and save images & text files in sequence
image_count = 0  # Track correct numbering

for line_number, url in enumerate(urls, start=1):
    if not url:  # Skip empty lines
        print(f"⚠️ Skipping empty line {line_number}")
        continue

    # Extract data
    img_url, username, title, date_taken, caption, hashtags, comments = extract_flickr_data(url)

    if not img_url:
        print(f"❌ No image found for {url}, skipping...")
        continue  # Skip if no image is found

    # Increment image count only for successful downloads
    image_count += 1

    try:
        # Download the image
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            img_path = os.path.join(output_folder, f"number{image_count}.jpg")
            with open(img_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            print(f"✅ Downloaded: {url} as number{image_count}.jpg")
        else:
            print(f"❌ Failed to download image from {url}")
            continue  # Skip to next URL

        # Save metadata to a text file
        text_file_path = os.path.join(output_folder, f"number{image_count}.txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(
                f"📌 Username: {username}\n"
                f"🗓️ Date: {date_taken}\n"
                f"📝 Title: {title}\n\n"
                f"📝 Caption:\n{caption}\n\n"
                f"🏷️ Hashtags: {hashtags}\n\n"
                f"💬 Comments:\n{comments}"
            )

        print(f"📝 Saved metadata as number{image_count}.txt")

    except Exception as e:
        print(f"❌ Error downloading {url}: {e}")

    # Delay to prevent rate limiting
    time.sleep(2)

print("🎉 Download completed! Check the 'flickr_downloads' folder.")
