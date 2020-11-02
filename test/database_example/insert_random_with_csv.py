# insert playlist's features into song_features, which is one of the database tables
# insertと書いてはいるが、spotifyから取ってきたプレイリストの特徴量をゲットして、tableの更新をすることである
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

    playlists = sp.current_user_playlists()['items'] # spotifyで自分で作ったプレイリストが入る
    update_table = ['random_selected'] # playlistsの中から更新するテーブルを選択する

    cur.execute("DROP TABLE IF EXISTS random_selected;")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS random_selected (
            index SERIAL,
            name VARCHAR(50) NOT NULL,
            uri VARCHAR(50) NOT NULL,
            acousticness DOUBLE PRECISION NOT NULL,
            danceability DOUBLE PRECISION NOT NULL,
            energy DOUBLE PRECISION NOT NULL,
            instrumentalness DOUBLE PRECISION NOT NULL,
            key DOUBLE PRECISION NOT NULL,
            liveness DOUBLE PRECISION NOT NULL,
            loudness DOUBLE PRECISION NOT NULL,
            mode DOUBLE PRECISION NOT NULL,
            speechiness DOUBLE PRECISION NOT NULL,
            tempo DOUBLE PRECISION NOT NULL,
            time_signature DOUBLE PRECISION NOT NULL,
            valence DOUBLE PRECISION NOT NULL,
            PRIMARY KEY (index)
        );
    """)
    for i, pl in enumerate(playlists):
        if pl['name'] in update_table:
            print(pl['name'])
            print('total tracks', pl['tracks']['total'])
            tracks = sp.playlist_tracks(pl['id'], fields="items.track.name, items.track.uri")
            #print(json.dumps(tracks, indent=4))
            for j, item in enumerate(tracks['items']):
                track = item['track']
                #print(json.dumps(sp.audio_features(track['uri']), indent=4))
                cur.execute("SELECT COUNT(index) FROM {};".format(pl['name'])) # primary_keyをあわせるためにcountしておく
                (cur_index, ) = cur.fetchone() # cur_indexはcurrent_index
                
                df = pd.DataFrame.from_dict(sp.audio_features(track['uri']))
                df = df.drop(labels=['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
                df.insert(loc=0, column='index', value=cur_index+1)
                df.insert(loc=1, column='name', value=track['name'])
                df.insert(loc=2, column='uri', value=track['uri'])

                print(df.cloumns)
                df.to_csv('csv/random_features.csv', header=False, index=False, encoding='utf-8')
                csv_file = open('csv/random_features.csv', mode='r', encoding='utf-8')
                cur.copy_expert("COPY random_selected FROM STDIN (FORMAT CSV, ENCODING 'UTF8');", csv_file)
                csv_file.close()
    conn.commit()
    cur.close()
    conn.close()