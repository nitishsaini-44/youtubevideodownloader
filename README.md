# YouTube Video Downloader

A simple and effective YouTube Video Downloader built with Python and Streamlit.

## Features

- **Fetch Video Details**: View thumbnail, title, author, and duration.
- **Multiple Resolutions**: Choose from available video resolutions (e.g., 360p, 720p, 1080p).
- **Audio Only**: Option to download audio only.
- **User-Friendly Interface**: Clean and intuitive UI using Streamlit.

## Installation

1.  Clone the repository or download the source code.
2.  Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

2.  Open your browser and navigate to the provided local URL (usually `http://localhost:8501`).
3.  Enter a YouTube URL and click "Fetch Video Details".
4.  Select your desired format and click "Download".

## Technologies Used

- **Streamlit**: For the web interface.
- **pytubefix**: For downloading YouTube content (reliable fork of pytube).
- **Requests**: For handling HTTP requests (if needed).
