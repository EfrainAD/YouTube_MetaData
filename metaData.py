from googleapiclient.discovery import build
from secrets import env_api_key

api_key = env_api_key
channel_id = "UCZ8OY0stb71wG6tJyxVWWKg" 

youtube = build('youtube', 'v3', developerKey=api_key)
request = youtube.videos().list(
    part="snippet,liveStreamingDetails",
)

search_response = youtube.search().list(
    part="id",
    channelId=channel_id,
    eventType="completed",
    order="date",
    type="video",
    maxResults=50,
).execute()

video_ids = [item['id']['videoId'] for item in search_response['items']]

if video_ids:
   videos_response = youtube.videos().list(
      part="snippet,liveStreamingDetails",
      id=",".join(video_ids)
   ).execute()

for video in videos_response['items']:
   snippet = video['snippet']
   streaming_date = video['liveStreamingDetails']['actualStartTime']
   date_only = streaming_date[:10]

   print('id:', video['id'])
   print('title:', snippet['title'])
   print('date:', date_only)
   print()
# print("Description:\n")
# print(snippet['description'], "\n")
