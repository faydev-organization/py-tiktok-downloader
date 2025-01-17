import yt_dlp
import os
import sys
import time
from pathlib import Path

def get_default_download_folder():
    home = Path.home()

    if sys.platform == "win32":
        return home / "Downloads"
    elif sys.platform == "darwin":
        return home / "Downloads"
    elif sys.platform == "linux" or sys.platform == "linux2":
        return home / "Downloads"
    else:
        raise Exception("Sistem operasi tidak dikenali untuk penentuan folder unduhan.")

def choose_download_folder(platform, url=None):
    base_folder = get_default_download_folder()

    if platform == "youtube":
        if "/shorts/" in url:
            platform_folder = os.path.join(base_folder, "youtube", "shorts")
        else:
            platform_folder = os.path.join(base_folder, "youtube")
    else:
        platform_folder = os.path.join(base_folder, platform)
    
    if not os.path.exists(platform_folder):
        os.makedirs(platform_folder)
    
    return platform_folder

def get_platform_from_url(url):
    if "x.com" in url:
        return "x"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "instagram.com" in url:
        return "instagram"
    elif "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    else:
        return "unknown"

def download_video(url, output_folder=None):
    if not output_folder:
        platform = get_platform_from_url(url)
        output_folder = choose_download_folder(platform, url)

    if not output_folder:
        sys.exit(1)

    platform = get_platform_from_url(url)

    if platform == "x":
        username = url.split('/')[3]
        tweet_id = url.split('/')[-1]
        filename_prefix = f"x_video_{username}_{tweet_id}"
    elif platform == "tiktok":
        username = url.split('/')[3]
        video_id = url.split('/')[-1]
        filename_prefix = f"tiktok_video_{username}_{video_id}"
    elif platform == "instagram":
        if "/reel/" in url:
            username = url.split('/')[3]
            reel_id = url.split('/')[-2]
            filename_prefix = f"instagram_reel_{username}_{reel_id}"
        elif "/p/" in url:
            username = url.split('/')[3]
            post_id = url.split('/')[-2]
            filename_prefix = f"instagram_post_{username}_{post_id}"
        else:
            print("URL Instagram tidak dikenali.")
            sys.exit(1)
    elif platform == "youtube":
        if "/shorts/" in url:
            shorts_id = url.split('/shorts/')[-1]
            filename_prefix = f"youtube_shorts_{shorts_id}"
        else:
            video_id = url.split('v=')[-1].split('&')[0]
            filename_prefix = f"youtube_video_{video_id}"
    else:
        print("Platform tidak dikenal.")
        sys.exit(1)

    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_folder, f"{filename_prefix}_%(id)s.%(ext)s"),
        'quiet': False,
        'verbose': False,
        'noplaylist': True,
        'extractaudio': False,
        'writeinfojson': False,
        'merge_output_format': 'mp4',
        'writethumbnail': False,
        'write_all_thumbnails': False,
        'force_generic_extractor': False,
        'extractor-retries': 3,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Konten berhasil diunduh dari {platform} dengan ID {filename_prefix}.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengunduh konten: {e}")
        sys.exit(1)

def download_multiple_videos(urls, output_folder=None):
    for url in urls:
        download_video(url, output_folder)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python script.py <URL1> <URL2> ...")
        sys.exit(1)

    urls = sys.argv[1:]

    download_multiple_videos(urls)
