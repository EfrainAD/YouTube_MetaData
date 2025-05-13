from googleapiclient.discovery import build
import subprocess
from secrets import env_api_key

api_key = env_api_key
channel_id = "UCZ8OY0stb71wG6tJyxVWWKg" 

def pause():
   input("Press Enter to continue... ")

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

youtube = build('youtube', 'v3', developerKey=api_key)

is_max_default = input_bool("Display last 10 videos? Or another ammount")
if is_max_default:
   maxResults = 10
else:
   maxResults = int(input("How many vidoe to display? (max is 50)\n"))

search_response = youtube.search().list(
    part="id",
    channelId=channel_id,
    eventType="completed",
    order="date",
    type="video",
    maxResults=maxResults,
).execute()

video_ids = [item['id']['videoId'] for item in search_response['items']]

if video_ids:
   videos_response = youtube.videos().list(
      part="snippet,liveStreamingDetails",
      id=",".join(video_ids)
   ).execute()

upload_format = input_bool("Display setting, that you want for when uploading videos to Spodify?")
print("\n")

videos = videos_response['items']

if upload_format:
   videos = videos[::-1]

for i, video in enumerate(videos, start=1):
   snippet = video['snippet']
   streaming_date = video['liveStreamingDetails']['actualStartTime']
   date_only = streaming_date[:10]
   title = snippet["title"]
   description = snippet["description"]

   # print('list id:', i)
   if not upload_format:
      print(f"#{i} 'Video Id: {video['id']}")
   print('date:', date_only)
   print(f"Title:\n------\n{title}\n------")
   if upload_format:
      copy_to_clipboard(title)
      pause()
   if upload_format:
      print(f"Description:\n-------\n{description}\n-------")
      copy_to_clipboard(description)
      pause()
   else:
      print()

   if upload_format:
      print()

