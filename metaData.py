from googleapiclient.discovery import build
import subprocess
from secrets import env_api_key

api_key = env_api_key
channel_id = "UCZ8OY0stb71wG6tJyxVWWKg" 

def pause():
   input("Press Enter to continue... ")
   print()

def copy_to_clipboard(text: str):
    subprocess.run('pbcopy', input=text.encode('utf-8'))
    print("Coyped to clipboard")

def input_bool(message):
   while True:
      user_input = input(f"{message}\ny/n ").lower()
      if user_input == 'y':
         return True
      elif user_input == 'n':
         return False
      print("Invalid entry.")

### MAIN ###
youtube = build('youtube', 'v3', developerKey=api_key)

print("To use the default value, just leave the input blank.")

user_input = input("How many vidoe to display? Defualt is 10 (max allowed is 50)\n")
if user_input.strip() in ("", "0"):
    maxResults = 10
else:
    maxResults = int(user_input)
    
# Get the playlist id that will be used to get the video list from.
channel_response = youtube.channels().list(
    part="contentDetails",
    id=channel_id
).execute()

upload_playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# Fetch video id's from upload playlist
if upload_playlist_id:
    playlist_response = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=upload_playlist_id,
        maxResults=maxResults
    ).execute()

video_ids = [item["contentDetails"]["videoId"] for item in playlist_response['items']]

upload_format = input_bool("Display setting, that you want for when uploading videos to Spotify?")
print("\n")

# Fetch the metadata for each video by id's
if video_ids:
    videos_response = youtube.videos().list(
        part="snippet,liveStreamingDetails",
        id=",".join(video_ids)
    ).execute()

    videos = videos_response["items"] or []
else:
    videos = []

if upload_format:
   videos = videos[::-1]

# Display each video's Data
for i, video in enumerate(videos, start=1):
    snippet = video['snippet']

    streaming_date = video['liveStreamingDetails']['actualStartTime']
    videoId = video["id"]
    date_only = streaming_date[:10]
    title = snippet["title"]
    file_name = title.replace(":", "_")
    description = snippet["description"]

    if not upload_format:
        print(f"#{i}")
        print("Video Id:", videoId)
        print("Title:", title)
        print("Date:", date_only)
        print()
    elif upload_format:
        # Copy File Name
        print(f"File Name:\n----------\n{file_name}\n----------")
        copy_to_clipboard(file_name)
        pause()

        # Copy Title
        print(f"Title:\n------\n{title}\n------")
        copy_to_clipboard(title)
        pause()

        # Copy Description
        print(f"Description:\n------------\n{description}\n------------")
        copy_to_clipboard(description)
        pause()

        # Display Date published, since this when you need it in the upload form
        print(f"Date:\n-----\n{date_only}\n-----")
        pause()
        print()
