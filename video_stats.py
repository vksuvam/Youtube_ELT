import requests
import json
import os
from dotenv import load_dotenv

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



if __name__ == "__main__":
    print("get playlist id will be executed")
    playlistId = get_playlist_id()
    print(get_video_id(playlistId))

# get_playlist_id()

