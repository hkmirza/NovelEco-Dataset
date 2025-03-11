import instaloader
import os
import time

# Initialize Instaloader
L = instaloader.Instaloader()

# **Login to Instagram (Required for full text access)**
USERNAME = "abcdef"  # Replace abcdef with your Instagram username
PASSWORD = "123456"  # Replace 123456 with your Instagram password

# Attempt to load session if previously saved
try:
    L.load_session_from_file(USERNAME)
    print("✅ Session loaded successfully.")
except FileNotFoundError:
    print("🔑 Logging into Instagram...")
    L.login(USERNAME, PASSWORD)
    L.save_session_to_file()

# Read Instagram URLs from a file
input_file = "instagram_urls.txt"  # Change this to your file containing URLs
output_folder = "downloads"
os.makedirs(output_folder, exist_ok=True)

# Load all lines from the file
with open(input_file, "r") as file:
    urls = [line.strip() for line in file]

# Process each line while maintaining its line number
for line_number, url in enumerate(urls, start=1):
    if not url:  # Skip empty lines
        print(f"⚠️ Skipping empty line {line_number}")
        continue

    try:
        short_code = url.split("/")[-2]  # Extract post shortcode
        post = instaloader.Post.from_shortcode(L.context, short_code)

        # 📸 Download the image(s)
        L.download_post(post, target=output_folder)
        time.sleep(1)  # Small delay to ensure file is free for renaming

        # Find and rename the latest downloaded file
        downloaded_files = sorted(
            [f for f in os.listdir(output_folder) if f.endswith(".jpg")],
            key=lambda x: os.path.getctime(os.path.join(output_folder, x)),  # Sort by creation time
            reverse=True  # Get the most recent file
        )

        if downloaded_files:
            latest_file = downloaded_files[0]  # Get the most recently downloaded file
            old_path = os.path.join(output_folder, latest_file)
            new_path = os.path.join(output_folder, f"number{line_number}.jpg")  # Use line number
            
            # Retry renaming if the file is in use
            retries = 3
            while retries > 0:
                try:
                    os.rename(old_path, new_path)
                    break
                except PermissionError:
                    print(f"⏳ Waiting to rename {latest_file}...")
                    time.sleep(2)
                    retries -= 1

            print(f"✅ Successfully downloaded: {url} as number{line_number}.jpg")
        else:
            print(f"❌ No image found for line {line_number}, skipping renaming.")

        # 📝 **Extract text data properly**
        username = post.owner_username
        post_date = post.date_utc.strftime("%Y-%m-%d %H:%M:%S")  # Date & time of post
        caption_text = post.caption if post.caption else "No caption available."
        likes = post.likes if post.likes else "Like count not available"
        hashtags = " ".join(post.caption_hashtags) if post.caption_hashtags else "No hashtags"

        # 💬 **Extract comments properly**
        comments_text = ""
        try:
            comments = post.get_comments()
            for comment in comments:
                comments_text += f"{comment.owner.username}: {comment.text}\n"
        except Exception as e:
            print(f"⚠️ Unable to retrieve comments for line {line_number}: {e}")
            comments_text = "Unable to retrieve comments."

        # 📝 **Save all extracted text data**
        text_file_path = os.path.join(output_folder, f"number{line_number}.txt")
        with open(text_file_path, "w", encoding="utf-8") as text_file:
            text_file.write(
                f"📌 Username: {username}\n"
                f"🗓️ Date: {post_date}\n"
                f"👍 Likes: {likes}\n"
                f"📝 Caption:\n{caption_text}\n\n"
                f"🏷️ Hashtags: {hashtags}\n\n"
                f"💬 Comments:\n{comments_text if comments_text else 'No comments'}"
            )

        print(f"📝 Saved all text data as number{line_number}.txt")

    except Exception as e:
        print(f"❌ Failed to download image or text from line {line_number}: {e}")

    # Delay to prevent rate limiting
    time.sleep(3)  # Adjust as needed

print("🎉 Download completed! Images and all text details saved as 'numberX.jpg' and 'numberX.txt'.")
