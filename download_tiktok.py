import yt_dlp
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog

def choose_download_folder():
    # Open a file dialog to choose the folder
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_selected = filedialog.askdirectory(title="Select Folder to Save the Video")

    # Return the folder path selected by the user
    return folder_selected

def download_tiktok_video(url, output_folder=None):
    if not output_folder:
        # If no folder was chosen, let the user pick a folder
        output_folder = choose_download_folder()

        # If user cancels, exit the script
        if not output_folder:
            sys.exit(1)

    # Use the video ID from the URL for naming the downloaded video
    video_id = url.split('/')[-1]
    output_path = os.path.join(output_folder, f"tiktok_video_{video_id}_{int(time.time())}.mp4")

    # yt-dlp options
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': False, 
        'verbose': False,  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        sys.exit(1)

def download_multiple_videos(urls, output_folder=None):
    for url in urls:
        download_tiktok_video(url, output_folder)

if __name__ == "__main__":
    # Check if URLs are provided as arguments
    if len(sys.argv) < 2:
        sys.exit(1)

    # Get all URLs from the command line arguments
    urls = sys.argv[1:]

    # Call the function to download all videos
    download_multiple_videos(urls)
