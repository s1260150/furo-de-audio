# insert playlist's features into database table 
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
# library for database 
import psycopg2 as pg2
from sqlalchemy import create_engine
import pandas as pd

#scope = 'playlist-modify-public'

if __name__ == '__main__':
    # configuration of database
    conn = {
        'user': "postgres",
        'password': "re64postgre",
        'host': "localhost",
        'port': "5432",
        'database': "spotify"
    }
    
    engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**conn))

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

    playlists = sp.current_user_playlists() # => myStreamR, myStreamY
    user_id = sp.me()['id'] # 自分のspotify上のIDが出る
    
    print('  total tracks', playlists['items'][1]['tracks']['total'])
    results = sp.playlist(playlists['items'][1]['id'], fields="tracks,next")
    tracks = results['tracks']
    #print(json.dumps(tracks, indent=4))

    for i, item in enumerate(tracks['items']):
        track = item['track']
        print(track['uri'])
        #print(json.dumps(sp.audio_features(track['uri']), indent=4))
        df = pd.DataFrame.from_dict(sp.audio_features(track["uri"]))
        df = df.drop(labels=['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
        df = df.reset_index(drop=True)
        #print(df)
        #df.to_sql('song_features', con=engine, if_exists='replace')

    #conn.close()