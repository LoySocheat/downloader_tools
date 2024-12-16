## Introduction

This script is designed to download videos from multiple platforms, including **TikTok**, **Instagram**, and **Kuaishou**. It automates the process of fetching and saving videos or images from these platforms, allowing you to input single URLs or batch process multiple videos through a text file.

## Features
- Download TikTok videos using TikTok URL.
- Download Instagram videos or images.
- Download Kuaishou videos.
- Download Youtube videos.
- Batch download multiple videos from a `.txt` file.

## How to Use

1. **Single TikTok Video Download:**
   - Choose the option to download a single video from TikTok.
   - Input the video URL when prompted.
   - The video will be saved in the `./tiktok` folder.

2. **Multiple TikTok Videos:**
   - Store TikTok video URLs in a `.txt` file, each on a new line.
   - Choose the option to download multiple TikTok videos from the file.
   - Input the file path when prompted, and the script will download all videos to the `./tiktok` folder.

3. **Single Instagram Video/Image Download:**
   - Choose the option to download an Instagram post.
   - Input the post URL when prompted.
   - The script will automatically detect whether the post is a video or an image and download it to the `./instagram` folder.

4. **Multiple Instagram Posts:**
   - Similar to TikTok, you can store Instagram URLs in a `.txt` file.
   - Choose the option to download multiple Instagram posts and input the file path.

5. **Single Kuaishou Video Download:**
   - Choose the option to download a single Kuaishou video.
   - Input the Kuaishou URL when prompted, and the video will be saved in the `./kuaishou` folder.

6. **Multiple Kuaishou Videos:**
   - Store Kuaishou URLs in a `.txt` file, and follow the prompts to batch download.

7. **Single Youtube Video Download:**
   - Choose the option to download a single Youtube video.
   - Input the Youtube URL when prompted, and the video will be saved in the `./youtube` folder.

8. **Multiple Youtube Videos:**
   - Store Youtube URLs in a `.txt` file, and follow the prompts to batch download.

9. **Exit the Program:**
   - Select the exit option to terminate the program.

### Prerequisites

1. **Install Python**  
   Make sure you have **Python 3.x** installed on your system. You can download it from [Python's official website](https://www.python.org/downloads/).
   
   To check if Python is installed, run the following command in your terminal or command prompt:

   ```bash
   python --version
   ```

2. **Set up environment variables:**

    - Create a `.env` file in the root of your project directory. This file should contain environment-specific variables that your application needs. 
    - Example in`.env.example` file

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/LoySocheat/downloader_tools
   ```

2. Navigate to the project directory:

   ```bash
   cd downloader_tools
   ```

3. Install the required packages:

   run setup.bat file

4. Run the script:

   Run downloader.bat file and follow the prompts to download videos
