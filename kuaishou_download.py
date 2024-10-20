import os
import requests
import string
import sys
import platform
import ctypes
from bs4 import BeautifulSoup
import json
from moviepy.editor import VideoFileClip, vfx
from typing import Optional, Tuple
from dotenv import load_dotenv

load_dotenv() 

def replace_chars(chars: str) -> str:
    return ''.join(c for c in chars if c not in string.punctuation).replace(' ', '').replace('\n', '').replace('\xa0', '').replace('\r', '')

def get_free_space() -> float:
    folder = os.path.abspath(sys.path[0])
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value / (1024 ** 3)  # Convert bytes to GB
    else:
        st = os.statvfs(folder)
        return st.f_bavail * st.f_frsize / (1024 ** 3)

def load_cookies_from_file(file_path: str) -> dict:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error loading cookies: {e}")
        return {}

def resolve_shortened_url(session: requests.Session, short_url: str) -> Optional[str]:
    try:
        response = session.get(short_url, allow_redirects=True, timeout=5)
        return response.url
    except requests.RequestException as e:
        print(f"Error resolving shortened URL: {e}")
        return None

def extract_video_info(session: requests.Session, page_url: str) -> Tuple[Optional[str], Optional[str]]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    try:
        response = session.get(page_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'lxml')
            scripts = soup.find_all('script')
            for script in scripts:
                if 'url' in script.text:
                    video_url = script.text.split('url":"')[1].split('",')[0].replace('\\u002F', '/')
                    video_title = soup.find('title').text if soup.find('title') else "video"
                    return video_url, video_title
        else:
            print(f"Failed to fetch video page, status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching video page: {e}")
    return None, None

def change_speed(input_path: str, output_path: str, speed_factor: float) -> None:
    try:
        video = VideoFileClip(input_path).fx(vfx.speedx, speed_factor)
        video.write_videofile(output_path, codec="libx264")
    except Exception as e:
        print(f"An error occurred while changing video speed: {e}")

def download_and_convert_video(video_url: str, video_name: str, speed_factor: float = 1.0) -> Optional[str]:
    path = 'kuaishou'
    video_name = replace_chars(video_name)
    os.makedirs(path, exist_ok=True)

    original_filepath = os.path.join(path, f'{video_name}.mp4')
    modified_filepath = os.path.join(path, f'{video_name}_modified.mp4')

    if os.path.exists(modified_filepath):
        print(f'{modified_filepath} >>> Already exists!')
        return modified_filepath

    try:
        video_content = requests.get(video_url, timeout=(3, 7)).content
        with open(original_filepath, 'wb') as f:
            f.write(video_content)

        change_speed(original_filepath, modified_filepath, speed_factor)
        os.remove(original_filepath)
        return modified_filepath
    except Exception as e:
        print(f'Error downloading or converting video: {e}')
        return None
    

def load_cookies_from_env() -> list:
    cookies = []
    i = 1

    while True:
        cookie_name = os.getenv(f'COOKIE_{i}_NAME')
        cookie_value = os.getenv(f'COOKIE_{i}_VALUE')
        cookie_domain = os.getenv(f'COOKIE_{i}_DOMAIN')

        if not cookie_name or not cookie_value or not cookie_domain:
            break

        cookies.append({
            'name': cookie_name,
            'value': cookie_value,
            'domain': cookie_domain
        })
        i += 1

    return cookies

# Initialize a session and load cookies from environment variables
session = requests.Session()
cookies = load_cookies_from_env()

# Add each cookie to the session
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'], domain=cookie['domain'])

def kuaishou(download_url, save_path):
    resolved_url = resolve_shortened_url(session, download_url)
    try:    
        if resolved_url:
            video_url, video_title = extract_video_info(session, resolved_url)
            if video_url:
                modified_filepath = download_and_convert_video(video_url, video_title, 1.3)
                if modified_filepath:
                    try:
                        return modified_filepath, video_title
                    except Exception as e:
                        print(f"Error moving video file: {e}")
                else:
                    print("Failed to download or convert video.")
            else:
                print("Failed to extract video information.")
        else:
            print("Failed to resolve shortened URL.")
        return None
    except Exception as e:
        print(f"Error processing video: {e}")
        return None