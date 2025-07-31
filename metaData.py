from googleapiclient.discovery import build
import subprocess
from secrets import env_api_key

api_key = env_api_key
max_video_limit = 50
channel_id = "UCZ8OY0stb71wG6tJyxVWWKg" 

def pause():
   input("Press Enter to continue... ")
   print()

def copy_to_clipboard(text: str):
    subprocess.run('pbcopy', input=text.encode('utf-8'))
    print("Copied to clipboard")

def input_bool(message):
   while True:
      user_input = input(f"{message}\ny/n ").lower()
      if user_input == 'y':
         return True
      elif user_input == 'n':
         return False
      print("Invalid entry.")

### MAIN ###
def main():
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Get User's Input
    print("To use the default value, just leave the input blank.")

    user_input = input("How many videos to display? Default is 10 (max allowed is 50)\n")
    max_results = min(max(1, int(user_input)), max_video_limit) if user_input.strip() not in ("", "0") else 10

    upload_display = input_bool("Display setting, that you want for when uploading videos to Spotify?")
    print()

    # Get the playlist id that will be used to get the video list from.
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=channel_id
    ).execute()

    upload_playlist_id = (channel_response.get("items", [{}])
                          [0]
                          .get("contentDetails", {})
                          .get("relatedPlaylists", {})
                          .get("uploads"))

    # This not a try catch for the purpose of handling this a different way.
    if not upload_playlist_id:
        print("Error: Upload playlist ID not found.")
        return

    # Fetch videos id's from the upload playlist by its id
    playlist_response = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=upload_playlist_id,
        maxResults=max_results
    ).execute()

    try:
        video_ids = [item["contentDetails"]["videoId"] for item in playlist_response['items']]
    except Exception as e:
        print("Error: Was not able to properly parse the video mata data.")
        print("Issue with:", e)
        return

    # Fetch the metadata for each video by id's
    videos_response = youtube.videos().list(
        part="snippet,liveStreamingDetails",
        id=",".join(video_ids)
    ).execute()

    videos = videos_response.get("items", [])
    if not videos:
        print("No channel data found.")
        return

    # Change order if the user is uploading videos
    if upload_display:
       videos = videos[::-1]

    # Display each video's Data
    for i, video in enumerate(videos, start=1):
        streaming_date = video.get('liveStreamingDetails', {}).get('actualStartTime', "N/A")
        video_id = video["id"]
        date_only = streaming_date[:10]
        title = video['snippet']["title"]
        file_name = title.replace(":", "_")
        description = video['snippet']["description"]

        if not upload_display:
            print(f"#{i}")
            print("Video Id:", video_id)
            print("Title:", title)
            print("Date:", date_only)
            print()
        else:
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
main()