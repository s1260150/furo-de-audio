# insert playlist's features into song_features, which is one of the database tables
# insertと書いてはいるが、spotifyから取ってきたプレイリストの特徴量をもとめて、tableの更新をすることである
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
# library for database
import psycopg2 as pg2
import pandas as pd

if __name__ == '__main__':
    # configuration of database
    conn = pg2.connect(
        user="postgres",
        password="re64postgre",
        host="localhost",
        port="5432",
        database="spotify"
    )
    cur = conn.cursor()

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())

    playlists = sp.current_user_playlists() # => playlist_r, playlist_y
    user_id = sp.me()['id'] # 自分のspotify上のIDが出る
    
    print('total tracks', playlists['items'][1]['tracks']['total'])
    results = sp.playlist(playlists['items'][1]['id'], fields="tracks")
    tracks = results['tracks']
    #print(json.dumps(tracks, indent=4))

    for i, item in enumerate(tracks['items']):
        track = item['track']
        #print(json.dumps(sp.audio_features(track['uri']), indent=4))
        cur.execute("SELECT COUNT(index) FROM song_features;") # primary keyにあわせるためにcountしておく
        (cur_index, ) = cur.fetchone()
        df = pd.DataFrame.from_dict(sp.audio_features(track["uri"]))
        df = df.drop(labels=['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
        df.insert(loc=0, column='index', value=cur_index+1)
        df.insert(loc=1, column='name', value=track['name'])
        df.insert(loc=2, column='uri', value=track['uri'])
        print(df.columns)
        df.to_csv('csv/features.csv', header=False, index=False)
        csv_file = open('csv/features.csv', mode='r', encoding='utf-8')
        cur.copy_from(csv_file, 'song_features', sep=',')
        csv_file.close()
    
    conn.commit()
    cur.close()
    conn.close()