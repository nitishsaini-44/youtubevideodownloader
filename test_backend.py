import downloader
import os

def test_backend():
    # Test URL (a short, safe video)
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" # Me at the zoo
    
    print(f"Testing with URL: {url}")
    
    # Test get_video_details
    print("Fetching details...")
    details = downloader.get_video_details(url)
    if "error" in details:
        print(f"FAILED: {details['error']}")
        return
    
    print(f"Title: {details['title']}")
    print(f"Author: {details['author']}")
    
    # Test get_available_streams
    print("Fetching streams...")
    streams = downloader.get_available_streams(details["object"])
    print(f"Found {len(streams)} streams.")
    
    if len(streams) > 0:
        print("First stream:", streams[0])
    
    print("Backend verification passed!")

if __name__ == "__main__":
    test_backend()
