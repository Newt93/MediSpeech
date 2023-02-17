import os
import pytube
import googleapiclient.discovery
from googleapiclient.errors import HttpError

# Set up the YouTube API client
def build_youtube_client(api_key):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
    return youtube

# Search for videos on a given topic
def search_videos(youtube, query, max_results=50):
    videos = []
    search_response = youtube.search().list(q=query, type='video', part='id,snippet', maxResults=max_results).execute()
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        title = search_result['snippet']['title']
        videos.append({'id': video_id, 'title': title})
    return videos

# Download the audio from a video
def download_audio(video_id):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    yt = pytube.YouTube(video_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path='videos', filename=f'{video_id}.mp4')
    return f'{video_id}.mp4'

# Extract audio clips from a video
def extract_clips(video_path):
    clip_path = os.path.splitext(video_path)[0]
    os.makedirs(clip_path, exist_ok=True)
    command = f'ffmpeg -i {video_path} -f segment -segment_time 15 -c copy {clip_path}/%03d.mp4'
    os.system(command)

# Main function
def main():
    # Set up the YouTube API client
    api_key = input('Enter your YouTube API key: ')
    youtube = build_youtube_client(api_key)

    # Search for videos on speech disorders
    query = input('Enter a query for speech disorder videos: ')
    videos = search_videos(youtube, query)

    # Download and process the videos
    for video in videos:
        print(f'Downloading {video["title"]}...')
        try:
            video_path = download_audio(video['id'])
            extract_clips(os.path.join('videos', video_path))
        except Exception as e:
            print(f'Error downloading {video["title"]}: {e}')

if __name__ == '__main__':
    main()
