import sys
import os
import argparse
import json
import yt_dlp

#* Settings
VIDEO_BEST_QUALITY = "bestvideo+bestaudio/best"
VIDEO_EXT = "mp4"

AUDIO_BEST_QUALITY = 'bestaudio/best'
AUDIO_EXT = "mp3"

# Config file name
CONFIG_FILE = 'config.json'


def load_config():
    """Load configuration from file, return dict with defaults if not exists."""
    defaults = {
        'output_dir': 'Download'
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key, value in defaults.items():
                    if key not in config:
                        config[key] = value
                return config
        except (json.JSONDecodeError, IOError):
            pass  # Fall back to defaults
    return defaults


def save_config(config):
    """Save configuration to file."""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except IOError:
        print(f"Warning: Could not save config to {CONFIG_FILE}")


#* Download Media from URLs
def download_media(urls, output_dir, formate, ext, no_playlist, is_video):
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
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Handle temp directory
    temp_dir = os.path.join(output_dir, 'Temp')
    os.makedirs(temp_dir, exist_ok=True)
    
    ydl_opts = {
        'format': formate,
        'postprocessors': postprocessors,
        'outtmpl': '%(title)s.%(ext)s', 
        'paths': {
            'home': output_dir,
            'temp': temp_dir
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
                print(f"[ERROR] {url}: {str(e)}")


# run script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download audio or video from URLs using yt-dlp.")
    parser.add_argument('urls', nargs='+', help="One or more URLs to download")
    parser.add_argument('--mode', choices=['audio', 'video'], default='audio', help="Download mode (default: audio)")
    parser.add_argument('--output-dir', help="Root output directory (if provided, saves as default for future runs)")
    parser.add_argument('--format', help="Custom format selector (overrides default based on mode)")
    parser.add_argument('--ext', help="Custom output extension (overrides default based on mode)")
    parser.add_argument('--quality', default='192', help="Audio quality (default: 192)")
    parser.add_argument('--no-playlist', action='store_true', help="Download single item instead of playlist")
    
    args = parser.parse_args()
    
    # Load persistent config
    config = load_config()
    
    # Handle output dir: use arg if provided (and save to config), else from config
    if args.output_dir:
        config['output_dir'] = args.output_dir
        save_config(config)
        root_output_dir = args.output_dir
    else:
        root_output_dir = config['output_dir']
    
    # Determine mode settings
    is_video = args.mode == 'video'
    default_format = VIDEO_BEST_QUALITY if is_video else AUDIO_BEST_QUALITY
    default_ext = VIDEO_EXT if is_video else AUDIO_EXT
    
    formate = args.format or default_format
    ext = args.ext or default_ext
    
    # Set output subdirectory
    sub_dir = "Video" if is_video else "Audio"
    output_dir = os.path.join(root_output_dir, sub_dir)
    
    # Download
    download_media(args.urls, output_dir, formate, ext, args.no_playlist, is_video)