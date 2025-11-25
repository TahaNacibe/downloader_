import sys
import os
import yt_dlp

#* Settings
VIDEO_BEST_QUALITY = "bestvideo+bestaudio/best"
VIDEO_EXT = "mp4"


AUDIO_BEST_QUALITY = 'bestaudio/best'
AUDIO_EXT = "mp3"


#* Download Audio from URLs
def download_audio(urls, output_dir="Download", formate=VIDEO_BEST_QUALITY, ext=VIDEO_EXT, no_playlist=False):
    
    if is_video:
        postprocessors = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': ext,
        }]
    else:
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': ext,      
            'preferredquality': '192',    
        }]
    # handle output directory
    ydl_opts = {
        'format': formate,
        'postprocessors': postprocessors,
        'outtmpl': '%(title)s.%(ext)s', 
        'paths':{
            'home': output_dir,
            'temp': os.path.abspath(f'{output_dir}/Temp/')
        },
        'noplaylist': no_playlist,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"[TARGET]: {url}")
                ydl.download([url])
                print(f"[DONE]: {url}")
            except Exception as e:
                print(f"[ERROR]/ {url}: {str(e)}")


# run script
if __name__ == "__main__":
    # settings
    is_video = False
    no_playlist = True
    
    # output directory
    root_output_dir = "Download"
    audio_dir = root_output_dir + "/Audio"
    video_dir = root_output_dir + "/Video"
    
    # download settings
    urls = ["https://www.youtube.com/shorts/nIZXgpGtGRQ"]
    formate = VIDEO_BEST_QUALITY if is_video else AUDIO_BEST_QUALITY
    ext = VIDEO_EXT if is_video else AUDIO_EXT
    output_dir = video_dir if is_video else audio_dir
    download_audio(urls, output_dir, formate, ext, no_playlist)