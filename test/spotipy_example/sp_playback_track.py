import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import time
import requests
import os
# library for database
import psycopg2 as pg2

# user-modify-playback => start_playback(), pause_playback(), skip(), volume()
# user-read-playback-state => devices()
scope = 'user-modify-playback-state user-read-playback-state'

if __name__ == '__main__':
    # configuration of database
    conn = pg2.connect(
        user="postgres",
        password="re64postgre",
        host="localhost",
        port="5432",
        database="spotify"
    )
    cursor = conn.cursor()
    print(os.environ.get("SPOTIPY_CLIENT_ID"))
    print(os.environ.get("SPOTIPY_REDIRECT_URI"))
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
        #client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
        #username=os.environ.get("SPOTIPY_CLIENT_USERNAME"),
        scope=scope)
    )
    token = sp._auth_manager.get_cached_token()
    print(token)
    
    expired = sp._auth_manager.is_token_expired(token)
    print(expired)

    for i in range(3):
        access_token = sp._auth_manager.refresh_access_token(token['refresh_token'])
        print(access_token)
    
    d_list = sp.devices()
    device_id = None
    for d in d_list['devices']:
        if d['name'] == 'raspotify (raspberrypi)':
            device_id = d['id']
    
    print("*** device id ***", device_id)
    cursor.execute("SELECT uri FROM playlist_r WHERE index = 1;")
    (uri, ) = cursor.fetchone()
    print("*** track id ***", uri)
    playback = sp.search(uri)
    print(json.dumps(playback, indent=4))

    sp.start_playback(device_id=device_id, uris=[uri])
    time.sleep(5) # wait 3 sec
    sp.pause_playback(device_id=device_id)