import requests
import os
import re
import time
import instaloader
import kuaishou_download

def get_response(url):
    """Get the response text from a URL."""
    r = requests.get(url)
    while r.status_code != 200:
        r = requests.get(url)
    return r.text

def clean_caption(caption):
    caption = caption.replace("\n", " ")
    caption = re.sub(r'[\\/*?:"<>|]', "", caption)
    caption = re.sub(r'[.!?;,\[\](){}&%@$^*\'"\\]', "", caption)
    caption = re.sub(r'\s+', ' ', caption)
    caption = caption[:150]
    
    return caption
def prepare_urls(matches):
    """Prepare unique URLs from regex matches."""
    return list({match.replace("\\u0026", "&") for match in matches})

def download_single_tiktok_video(video_url):
    """Download a single TikTok video."""
    try:
        api_url = "https://www.tikwm.com/api/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        params = {"url": video_url}
        response = requests.get(api_url, headers=headers, params=params)
        data = response.json()

        if data['code'] == 0:
            video_data = data['data']
            video_download_url = video_data['play']
            video_id = video_data['id']

            if not os.path.exists("./tiktok"):
                os.makedirs("./tiktok")

            start = time.time()
            video_bytes = requests.get(video_download_url, stream=True)
            with open(f'./tiktok/{video_id}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
                end = time.time()

            elapsed_time = end - start
            print(f"[Programs] [Status] Timelapse: {elapsed_time:.2f}s")
            print(f"[Programs] [File] {video_id}.mp4 Downloaded")

        else:
            print("[Error] Failed to download TikTok video. Please check the URL and try again.")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_single_instagram_video(video_url):
    """Download a single Instagram video or image."""
    try:
        response = get_response(video_url)

        vid_matches = re.findall('"video_url":"([^"]+)"', response)
        pic_matches = re.findall('"display_url":"([^"]+)"', response)

        vid_urls = prepare_urls(vid_matches)
        pic_urls = prepare_urls(pic_matches)

        if not os.path.exists("./instagram"):
            os.makedirs("./instagram")

        if vid_urls:
            for index, vid_url in enumerate(vid_urls):
                start = time.time()
                video_bytes = requests.get(vid_url, stream=True)
                with open(f'./instagram/video_{index}.mp4', 'wb') as out_file:
                    out_file.write(video_bytes.content)
                end = time.time()

                elapsed_time = end - start
                print(f"[Programs] [Status] Timelapse: {elapsed_time:.2f}s")
                print(f"[Programs] [File] video_{index}.mp4 Downloaded")

        if pic_urls:
            for index, pic_url in enumerate(pic_urls):
                start = time.time()
                image_bytes = requests.get(pic_url, stream=True)
                with open(f'./instagram/image_{index}.jpg', 'wb') as out_file:
                    out_file.write(image_bytes.content)
                end = time.time()

                elapsed_time = end - start
                print(f"[Programs] [Status] Timelapse: {elapsed_time:.2f}s")
                print(f"[Programs] [File] image_{index}.jpg Downloaded")

        if not (vid_urls or pic_urls):
            print('Could not recognize the media in the provided URL.')

    except Exception as e:
        print(f"An error occurred: {e}")

def download_multiple_videos_tiktok(video_urls, platform):
    """Download multiple videos from a list of URLs based on the platform."""
    for video_url in video_urls:
        try:
            if platform == "tiktok":
                download_single_tiktok_video(video_url)
            elif platform == "instagram":
                download_single_instagram_video(video_url)
        except Exception as e:
            print(f"[Error] An error occurred while downloading video from {video_url}: {e}")

def read_urls_from_file(file_path):
    """Read video URLs from a .txt file."""
    video_urls = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                if url:
                    video_urls.append(url)
    except FileNotFoundError:
        print(f"[Error] File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
    
    return video_urls

def download_single_instagram_video_or_image(post_url):
    """Download Instagram video or image using Instaloader."""
    L = instaloader.Instaloader()
    
    try:
        shortcode = post_url.split('/')[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        if not os.path.exists("./instagram"):
            os.makedirs("./instagram")
            
        caption = clean_caption(post.caption)

        if caption:
            sanitized_title = caption
        else:
            sanitized_title = shortcode
            
        if post.is_video:
            video_url = post.video_url
            start = time.time()
            video_bytes = requests.get(video_url, stream=True)
            with open(f'./instagram/{sanitized_title}.mp4', 'wb') as out_file:
                out_file.write(video_bytes.content)
            end = time.time()

            elapsed_time = end - start
            print(f"[Programs] [Status] Timelapse: {elapsed_time:.2f}s")
            print(f"[Programs] [File] {sanitized_title}.mp4 Downloaded")
        else:
            image_url = post.url
            start = time.time()
            image_bytes = requests.get(image_url, stream=True)
            with open(f'./instagram/{sanitized_title}.jpg', 'wb') as out_file:
                out_file.write(image_bytes.content)
            end = time.time()

            elapsed_time = end - start
            print(f"[Programs] [Status] Timelapse: {elapsed_time:.2f}s")
            print(f"[Programs] [File] {sanitized_title}.jpg Downloaded")

    except Exception as e:
        print(f"An error occurred: {e}")

def get_user_choice():
    """Get user choice for the download operation."""
    while True:
        print("\nChoose an option:")
        print("1. Download a single TikTok video")
        print("2. Download multiple TikTok videos from a .txt file")
        print("3. Download a single Instagram video")
        print("4. Download multiple Instagram videos from a .txt file")
        print("5. Download a single Kuaishou video")
        print("6. Download multiple Kuaishou videos from a .txt file")
        print("7. Exit")

        choice = input("Enter your choice (1, 2, 3, 4, 5, 6 or 7): ")
        if choice in ['1', '2', '3', '4', '5', '6', '7']:
            return choice
        else:
            print("[Error] Invalid choice. Please enter 1, 2, 3, 4, 5, 6 or 7.")
        
def main():
    """Main function to handle user input and video downloads."""
    while True:
        choice = get_user_choice()

        if choice == '1':
            video_url = input("Enter the TikTok video URL: ")
            download_single_tiktok_video(video_url)
        elif choice == '2':
            file_path = input("Enter the path to your .txt file containing TikTok URLs: ")
            video_urls = read_urls_from_file(file_path)
            if video_urls:
                download_multiple_videos_tiktok(video_urls, "tiktok")
            else:
                print("[Error] No URLs found in the file.")
        elif choice == '3':
            post_url = input("Enter the Instagram post URL: ")
            download_single_instagram_video_or_image(post_url)
        elif choice == '4':
            file_path = input("Enter the path to your .txt file containing Instagram URLs: ")
            video_urls = read_urls_from_file(file_path)
            if video_urls:
                for url in video_urls:
                    download_single_instagram_video_or_image(url)
            else:
                print("[Error] No URLs found in the file.")
                
        elif choice == '5':
            video_url = input("Enter the Kuaishou URL: ")
            kuaishou_download.kuaishou(video_url, 'kuaishou')
            
        elif choice == '6':
            print("Example: Kuaishou URL\nhttps://v.kuaishou.com/XXXXXX")
            file_path = input("Enter the path to your .txt file containing Kauishou URLs: ")
            video_urls = read_urls_from_file(file_path)
            if video_urls:
                for url in video_urls:
                    kuaishou_download.kuaishou(url, 'kuaishou')
            else: 
                print("[Error] No URLs found in the file.")

        elif choice == '7':
            print("Exiting the program.")
            break

        continue_choice = input("Do you want to go back to the main menu? (yes/no): ")
        if continue_choice.lower() != 'yes':
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()