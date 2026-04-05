import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path = './.env')

API_KEY = os.getenv('API_KEY')

CHANNEL_HANDLE = "AIEdgeHQ"


def get_playlist_id():

    try:
    
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)
        # print(response)

        response.raise_for_status()

        data = response.json()
        # print(json.dumps(data, indent = 4))

        channel_items = data["items"][0] #output: {'kind': 'youtube#channel', 'etag': 'KDEnWSxpY22O5fBNwOw98F-H50g', 'id': 'UC-PQKtrPhk3JXyjUleBLgQQ', 'contentDetails': {'relatedPlaylists': {'likes': '', 'uploads': 'UU-PQKtrPhk3JXyjUleBLgQQ'}}}
        # print(channel_items)

        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]['uploads']
        print(channel_playlistId) #output: UU-PQKtrPhk3JXyjUleBLgQQ
        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Failed to fetch playlist ID: {e}') from e
    

if __name__ == "__main__":
    print("get playlist id will be executed")
    get_playlist_id()

# get_playlist_id()

