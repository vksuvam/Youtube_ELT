import requests
import json
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv(dotenv_path = './.env')

API_KEY = os.getenv('API_KEY')

CHANNEL_HANDLE = "AIEdgeHQ"
MAXRESULTS = 10

## get playlist id 
def get_playlist_id():

    ##using try catch block to handle exceptions, so that the program doesnt end abruptly and gives a meaningful error message
    try:
        
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        ## get url response
        response = requests.get(url)
        # print(response)

        ## raising for status in case we dont receive a response, this makes sure that function doesnt proceed and instead it goes into except block and raises the exception
        response.raise_for_status()
        
        ## converting response into json format
        data = response.json()
        # print(json.dumps(data, indent = 4))

        ## extracting channel items from json 
        channel_items = data["items"][0] #output: {'kind': 'youtube#channel', 'etag': 'KDEnWSxpY22O5fBNwOw98F-H50g', 'id': 'UC-PQKtrPhk3JXyjUleBLgQQ', 'contentDetails': {'relatedPlaylists': {'likes': '', 'uploads': 'UU-PQKtrPhk3JXyjUleBLgQQ'}}}
        # print(channel_items)

        ## extracting channel playlist ID from channel items
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]['uploads']
        # print(channel_playlistId) #output: UU-PQKtrPhk3JXyjUleBLgQQ
        return channel_playlistId

    ## using except block to raise exception 
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'Failed to fetch playlist ID: {e}') from e
    

## get video id
def get_video_id(playlistId):

    ## initializing empty array for video ids; will be used to append extracted video ids
    video_ids =[]
    
    ## setting pageToken to None as the first page doesnt give pageToken
    pageToken = None

    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={MAXRESULTS}&playlistId={playlistId}&key={API_KEY}"

    try:
        ## using while loop, so that we loop through all pages until last page of the channel playlist
        while True:

            url = base_url

            ## if the value of pageToken is true, we are appending the f to the base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            ## using the base url to get response
            response = requests.get(url)

            ## raising for status in case of HTMl error while getting the response
            response.raise_for_status()

            ## converting response to json format
            data = response.json()

            ## using for loop to loop through items within a page
            for item in data.get('items', []): #
                video_id = item['contentDetails']['videoId']  ## extracting video id from every items present in a page
                video_ids.append(video_id) ## insert video id into video_id array
            
            ## updating the value of pageToken 
            pageToken = data.get('nextPageToken')

            ## ending the while loop if pageToken value is nothing
            if not pageToken:
                break
        
        return video_ids

    
    ## raising exception
    except requests.exceptions.RequestException as e:
        raise e



def extract_video_data(video_ids):
    extracted_data = []

    def batch_list(video_id_lst, batch_size):
        for video_id in range(0, len(video_id_lst), batch_size):
            yield video_id_lst[video_id: video_id + batch_size]
        
    try:
        for batch in batch_list(video_ids, MAXRESULTS):
            video_id_str = ",".join(batch)

            url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=statistics&part=snippet&id={video_id_str}&key={API_KEY}'

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get('items', []):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
            
                video_data = {
                    "video_id": video_id,
                    "title": snippet['title'],
                    "publishedAt": snippet['publishedAt'],
                    "duration": contentDetails['duration'],
                    "viewCount":statistics.get('viewCount', None),
                    "likeCount":statistics.get('likeCount', None),
                    "commentCount":statistics.get('commentCount', None)
                }

                extracted_data.append(video_data)

        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


def save_to_json(extracted_data):
    file_path = f'./data/YT_data_{date.today()}.json'

    with open(file_path, "w", encoding ="utf-8") as json_outfile:
        json.dump(extracted_data, json_outfile, indent = 4, ensure_ascii = False)

if __name__ == "__main__":
    print("Fetching Playlist ID from the YT channel")
    playlistId = get_playlist_id()
    print("Fetching list of Video ID")
    video_ids = get_video_id(playlistId)
    print("Extracting video data")
    video_data = extract_video_data(video_ids)
    print("Saving extracted video data in json file")
    save_to_json(video_data)

# get_playlist_id()

