import streamlit as st
import downloader
import os

# Page Config
st.set_page_config(page_title="YouTube Video Downloader", page_icon="📹", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #FF0000;
        color: white;
    }
    .stButton>button:hover {
        background-color: #CC0000;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📹 YouTube Video Downloader")
st.markdown("Download your favorite YouTube videos easily in multiple resolutions.")

# Input
url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if "video_details" not in st.session_state:
    st.session_state.video_details = None
if "streams" not in st.session_state:
    st.session_state.streams = None

if st.button("Fetch Video Details"):
    if url:
        with st.spinner("Fetching details..."):
            details = downloader.get_video_details(url)
            if "error" in details:
                st.error(f"Error: {details['error']}")
            else:
                st.session_state.video_details = details
                st.session_state.streams = downloader.get_available_streams(details["object"])
    else:
        st.warning("Please enter a valid URL.")

# Display Details
if st.session_state.video_details:
    details = st.session_state.video_details
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(details["thumbnail"], width="stretch")
    
    with col2:
        st.subheader(details["title"])
        st.write(f"**Author:** {details['author']}")
        st.write(f"**Length:** {details['length']} seconds")
        st.write(f"**Views:** {details['views']:,}")
        st.write(f"**Published:** {details['publish_date']}")

    st.divider()
    
    # Download Section
    st.subheader("Download Options")
    
    if st.session_state.streams:
        streams = st.session_state.streams
        
        # Format options for selectbox
        options_map = {}
        for s in streams:
            label = f"{s['type'].upper()} - {s['resolution']} ({s['mime_type']}) - ~{s['filesize']:.2f} MB"
            options_map[label] = s['itag']
        
        selected_option = st.selectbox("Select Format:", list(options_map.keys()))
        
        if st.button("Download"):
            selected_itag = options_map[selected_option]
            with st.spinner("Downloading..."):
                # Create downloads directory if not exists
                if not os.path.exists("downloads"):
                    os.makedirs("downloads")
                
                file_path = downloader.download_stream(details["object"], selected_itag, "downloads")
                
                if file_path and not file_path.startswith("Error"):
                    st.success(f"Download Complete! Saved to: {file_path}")
                    
                    # Read file for download button
                    with open(file_path, "rb") as f:
                        file_bytes = f.read()
                        file_name = os.path.basename(file_path)
                        st.download_button(
                            label="Click to Save File",
                            data=file_bytes,
                            file_name=file_name,
                            mime="application/octet-stream"
                        )
                else:
                    st.error(f"Download failed: {file_path}")

