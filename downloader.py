from pytubefix import YouTube
from pytubefix.cli import on_progress
import os

def get_video_details(url):
    """
    Extracts video details from the given YouTube URL.
    """
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        return {
            "title": yt.title,
            "author": yt.author,
            "thumbnail": yt.thumbnail_url,
            "length": yt.length,
            "views": yt.views,
            "publish_date": yt.publish_date,
            "object": yt # Return the object to avoid re-initializing
        }
    except Exception as e:
        return {"error": str(e)}

def get_available_streams(yt_object):
    """
    Returns available video and audio streams.
    """
    try:
        streams = yt_object.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
        audio_streams = yt_object.streams.filter(only_audio=True).order_by('abr').desc()
        
        options = []
        # Video options
        for stream in streams:
            options.append({
                "type": "video",
                "resolution": stream.resolution,
                "mime_type": stream.mime_type,
                "itag": stream.itag,
                "filesize": stream.filesize_approx / (1024 * 1024) # MB
            })
            
        # Audio options
        for stream in audio_streams:
             options.append({
                "type": "audio",
                "resolution": stream.abr,
                "mime_type": stream.mime_type,
                "itag": stream.itag,
                "filesize": stream.filesize_approx / (1024 * 1024) # MB
            })
            
        return options
    except Exception as e:
        return []

def download_stream(yt_object, itag, download_path="."):
    """
    Downloads the stream with the given itag.
    Returns: (file_path, error_message)
    """
    try:
        stream = yt_object.streams.get_by_itag(itag)
        if stream:
            file_path = stream.download(output_path=download_path)
            return file_path, None
        return None, "Stream not found"
    except Exception as e:
        return None, str(e)
