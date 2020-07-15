# insert playlist's features into song_features, which is one of the database tables
# insertと書いてはいるが、spotifyから取ってきたプレイリストの特徴量をもとめて、tableの更新をすることである
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
# library for database
import psycopg2 as pg2
import pandas as pd
import os

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

    playlists = sp.current_user_playlists()['items'] # => 自分で作ったプレイリストが入る
    user_id = sp.me()['id'] # 自分のspotify上のIDが出る
    update_table = ['random_selected'] # playlistsの中から更新するテーブルを選択する

    for i, pl in enumerate(playlists):
        print(pl['name'])
        print('total tracks', pl['tracks']['total'])

        if pl['name'] in update_table:
            print('total tracks before update: ', pl['tracks']['total'])
            tracks = sp.playlist_tracks(pl['id'], fields="items.track.name, items.track.uri")
            #print(json.dumps(tracks, indent=4))
            for j, item in enumerate(tracks['items']):
                track = item['track']
                #print(json.dumps(sp.audio_features(track['uri']), indent=4))
                cur.execute("SELECT COUNT(index) FROM {};".format(pl['name'])) # primary keyにあわせるためにcountしておく
                (cur_index, ) = cur.fetchone() # cur_indexはcurrent_indexです
                
                df = pd.DataFrame.from_dict(sp.audio_features(track['uri']))
                df = df.drop(labels=['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
                df.insert(loc=0, column='index', value=cur_index+1)
                df.insert(loc=1, column='name', value=track['name'])
                df.insert(loc=2, column='uri', value=track['uri'])
                #print(df)
                df.to_csv('csv/random_features.csv', header=False, index=False)
                csv_file = open('csv/random_features.csv', mode='r', encoding='utf-8')
                cur.copy_expert("COPY random_selected FROM STDIN (FORMAT CSV, ENCODING 'UTF8');", csv_file)
                csv_file.close()
    conn.commit()
    cur.close()
    conn.close()