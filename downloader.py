import yt_dlp
import os

def get_video_details(url):
    """
    Extracts video details using yt-dlp.
    """
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title'),
                "author": info.get('uploader'),
                "thumbnail": info.get('thumbnail'),
                "length": info.get('duration'),
                "views": info.get('view_count'),
                "publish_date": info.get('upload_date'),
                "webpage_url": info.get('webpage_url'),
                "formats": info.get('formats', [])
            }
    except Exception as e:
        return {"error": str(e)}

def get_available_streams(details):
    """
    Returns available formats from the details dictionary.
    Filters for mp4 video (progressive) and best audio.
    """
    try:
        formats = details.get("formats", [])
        options = []
        
        # Filter for video+audio (progressive) - usually 720p/360p
        # yt-dlp marks these as having both vcodec and acodec != 'none'
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('ext') == 'mp4':
                filesize = f.get('filesize') or f.get('filesize_approx') or 0
                options.append({
                    "type": "video",
                    "resolution": f.get('format_note') or f"{f.get('height')}p",
                    "mime_type": "video/mp4",
                    "format_id": f['format_id'],
                    "filesize": filesize / (1024 * 1024) # MB
                })
        
        # Filter for audio only (m4a/mp3)
        for f in formats:
            if f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                filesize = f.get('filesize') or f.get('filesize_approx') or 0
                options.append({
                    "type": "audio",
                    "resolution": f"{int(f.get('abr', 0))}kbps",
                    "mime_type": f"audio/{f.get('ext')}",
                    "format_id": f['format_id'],
                    "filesize": filesize / (1024 * 1024) # MB
                })
                
        # Sort options (simple sort by type then resolution)
        options.sort(key=lambda x: (x['type'], x['resolution']), reverse=True)
        return options
    except Exception as e:
        return []

def download_stream(url, format_id, download_path="."):
    """
    Downloads the stream with the given format_id using yt-dlp.
    Returns: (file_path, error_message)
    """
    try:
        ydl_opts = {
            'format': format_id,
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Download
            ydl.download([url])
            
            # Get filename
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Verify file exists (sometimes extension changes)
            if os.path.exists(filename):
                return filename, None
            else:
                # Try to find the file if extension changed (e.g. mkv -> mp4)
                # This is a basic check, might need more robust logic
                base, _ = os.path.splitext(filename)
                for ext in ['.mp4', '.mkv', '.webm', '.m4a', '.mp3']:
                    if os.path.exists(base + ext):
                        return base + ext, None
                
            return filename, None # Return expected name even if check failed (or handle error)
    except Exception as e:
        return None, str(e)
