# Search artists and add their songs to a user's playlists (need to be authenticated via oauth)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
scope = 'playlist-modify-public'

if __name__ == '__main__':
    
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlists = sp.current_user_playlists() # => myStreamR, myStreamY
    user_id = sp.me()['id'] # 自分のspotify上のIDが出る
    """
    print(playlists['items'][0]['name'])
    for playlist in playlists['items']:
        if playlist['owner']['id'] == user_id:
    """
    #sp.start_playback()
    search = sp.search(q="bfmv", limit=4, type="track")
    #print(json.dumps(search, indent=4))

    for i, track in enumerate(search["tracks"]["items"]):
        print(track["uri"], track["name"])
        #sp.user_playlist_add_tracks(user_id, playlist['id'], [track["id"]])
        features = sp.audio_features(track["uri"])
        print(json.dumps(features, indent=4))