import yt_dlp
import os
import sys
import time
import platform

def choose_download_folder():
    # Menentukan lokasi folder berdasarkan sistem operasi
    system_platform = platform.system().lower()
    
    if system_platform == 'windows':  # Untuk Windows
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif system_platform == 'darwin':  # Untuk macOS
        return os.path.join(os.path.expanduser("~"), "Desktop")
    elif system_platform == 'linux':  # Untuk Linux
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:  # Untuk Android
        # Menentukan folder default di Android (Movies atau Pictures)
        # Folder Movies di perangkat Android yang mendukung galeri
        return os.path.join(os.path.expanduser("~"), "Movies")

def download_tiktok_video(url, output_folder=None):
    if not output_folder:
        # Jika tidak ada folder yang dipilih, gunakan folder default berdasarkan platform
        output_folder = choose_download_folder()

    # Jika folder tidak valid, keluar dari script
    if not output_folder:
        sys.exit(1)

    # Gunakan video ID dari URL untuk penamaan file video yang diunduh
    video_id = url.split('/')[-1]
    output_path = os.path.join(output_folder, f"tiktok_video_{video_id}_{int(time.time())}.mp4")

    # Opsi yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'quiet': False,
        'verbose': False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Video berhasil diunduh di: {output_path}")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengunduh video: {e}")
        sys.exit(1)

def download_multiple_videos(urls, output_folder=None):
    for url in urls:
        download_tiktok_video(url, output_folder)

if __name__ == "__main__":
    # Memeriksa apakah URL diberikan sebagai argumen
    if len(sys.argv) < 2:
        print("Penggunaan: python script.py <URL1> <URL2> ...")
        sys.exit(1)

    # Mendapatkan semua URL dari argumen baris perintah
    urls = sys.argv[1:]

    # Memanggil fungsi untuk mengunduh semua video
    download_multiple_videos(urls)
