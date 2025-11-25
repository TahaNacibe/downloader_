# YouTube Media Downloader

A simple command-line Python script using `yt-dlp` to download audio or video from YouTube (and other supported sites). Supports batch downloads, custom formats, persistent output directory configuration, and post-processing (e.g., converting to MP3/MP4 with FFmpeg).

## Features
- Download single videos/shorts or entire playlists (with option to disable).
- Audio extraction (MP3, 192kbps default) or full video (MP4, best quality default).
- Persistent configuration (e.g., default output directory saved to `config.json`).
- Customizable format selectors and output extensions.
- Automatic directory creation (e.g., `./Download/Audio/` or `./Download/Video/`).

## Requirements
- Python 3.6+.
- `yt-dlp` library: Install with `pip install yt-dlp`.
- FFmpeg: Required for post-processing (audio extraction/video conversion).
  - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.
  - **macOS**: `brew install ffmpeg`.
  - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install ffmpeg`.

## Installation
1. Clone or download this script as `downloader.py`.
2. Install dependencies: `pip install yt-dlp`.
3. Ensure FFmpeg is installed and accessible via command line (`ffmpeg -version` should work).

## Usage
Run the script from the command line/terminal:

```
python downloader.py <URL1> [URL2 ...] [options]
```

- **URLs**: Positional arguments. One or more YouTube (or compatible) URLs. Enclose in quotes if they contain spaces/special characters.
- **Options**: See below for flags.

### Basic Examples

1. **Download audio from a single Short (default mode):**
   ```
   python downloader.py "https://www.youtube.com/shorts/nIZXgpGtGRQ"
   ```
   - Saves as MP3 to `./Download/Audio/` (creates directories if needed).

2. **Download video from multiple URLs:**
   ```
   python downloader.py "https://www.youtube.com/watch?v=example1" "https://www.youtube.com/watch?v=example2" --mode video
   ```
   - Saves as MP4 to `./Download/Video/`.

3. **Set custom output directory (saves as default for future runs):**
   ```
   python downloader.py "https://www.youtube.com/shorts/nIZXgpGtGRQ" --output-dir "C:\MyDownloads"
   ```
   - Saves to `C:\MyDownloads\Audio\`. Future runs without `--output-dir` use this path.

4. **Download single item from a playlist:**
   ```
   python downloader.py "https://www.youtube.com/playlist?list=example" --no-playlist --mode audio
   ```
   - Downloads only the first item as audio.

5. **Custom format, extension, and quality:**
   ```
   python downloader.py "https://www.youtube.com/watch?v=example" --mode video --format "worstvideo" --ext "avi" --quality 128
   ```
   - Downloads low-quality AVI video. (Quality flag applies only to audio mode.)

6. **Full example using all options:**
   ```
   python downloader.py "https://www.youtube.com/watch?v=example1" "https://www.youtube.com/watch?v=example2" --mode video --output-dir "/path/to/custom/downloads" --format "bestvideo+bestaudio/best" --ext "mp4" --quality 128 --no-playlist
   ```
   - Downloads two single videos as MP4 (best quality) to `/path/to/custom/downloads/Video/`.

### Options
| Flag | Description | Example | Default |
|------|-------------|---------|---------|
| `--mode` | Download type: `audio` or `video`. | `--mode video` | `audio` |
| `--output-dir` | Root output folder (saves to `config.json` if provided). | `--output-dir "~/Music/Downloads"` | `./Download` (from config) |
| `--format` | yt-dlp format selector (overrides mode default). | `--format "bestaudio[abr>128]"` | `bestaudio/best` (audio) or `bestvideo+bestaudio/best` (video) |
| `--ext` | Output file extension. | `--ext "m4a"` | `mp3` (audio) or `mp4` (video) |
| `--quality` | Audio bitrate (kbps; only for audio mode). | `--quality 320` | `192` |
| `--no-playlist` | Download only single item (ignore playlists). | (flag) | `False` (downloads full playlist if detected) |

Run `python downloader.py --help` for full argparse help.

## Configuration
- The script uses a `config.json` file in the script's directory to store defaults (e.g., `output_dir`).
- Providing `--output-dir` updates and saves it permanently.
- Manually edit `config.json` to tweak:
  ```json
  {
      "output_dir": "Download"
  }
  ```
- Currently only `output_dir` is persisted; extend the script's `load_config()` for more.

## Output Structure
- Root: Specified output dir (default: `./Download`).
- Subdirs: `/Audio/` for audio, `/Video/` for video, `/Temp/` for temporary files (auto-cleaned by yt-dlp).
- Files: Named by title, e.g., `Video Title.mp4`.

## Troubleshooting
- **FFmpeg not found**: Install FFmpeg and ensure it's in your PATH. Test with `ffmpeg -version`.
- **Download fails**: Check URL validity. yt-dlp handles rate limits/errors; see console output.
- **Permission errors**: Run as admin or check folder write access.
- **No audio/video**: Ensure site is supported (yt-dlp docs: [formats](https://github.com/yt-dlp/yt-dlp#format-selection)).
- **Config issues**: Delete `config.json` to reset to defaults.

## License
MIT License. Feel free to modify/fork.

## Credits
Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp). For advanced usage, see yt-dlp docs.