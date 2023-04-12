import datetime
from apiclient.discovery import build

YOUTUBE_API_KEY = 'enter youtube_api_key here'
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def YouTubelist(nPT,channnel):
    search_response = youtube.search().list(
        channelId=channnel,
        part='snippet',
        maxResults=50,
        order='date',
        type='video',
        pageToken=nPT
    ).execute()

    video_ids = []
    items = search_response['items']
    for item in items :
        video_ids.append(item['id']['videoId'])

    details = youtube.videos().list(
        part='liveStreamingDetails',
        id=video_ids
    ).execute()
    detailitems = details['items']

    JST = datetime.timedelta(hours=9)
    def timetrans(strtime):
        stime = datetime.datetime.fromisoformat(strtime[:-1]) + JST
        return stime.replace(microsecond=0)

    csvdata = []
    for item, detail in zip(items, detailitems):

        title = item['snippet']['title']
        video_id = item['id']['videoId']

        state = item['snippet']['liveBroadcastContent']
        if state == 'upcoming':
            starttime = timetrans(detail['liveStreamingDetails']['scheduledStartTime'])

        if state == 'upcoming':
            print('https://www.youtube.com/watch?v='+video_id,'|',title,'|',starttime)

    return search_response['nextPageToken'], csvdata

if __name__ == "__main__":
    print(YouTubelist(None, 'UCB7V8MLk5ZcwQjtgN8xCowA'))
