# insert playlist's features into song_features, which is one of the database tables
# insertと書いてはいるが、spotifyから取ってきたプレイリストの特徴量をゲットして、tableの更新をすることである
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

    playlists = sp.current_user_playlists()['items'] # spotifyで自分で作ったプレイリストが入る
    update_table = {
        'playlist_r': 'song_features_r', # (key, value) = (song to extract features, table for features)
        'playlist_y': 'song_features_y', # (key, value) = (song to extract features, table for features)
    }# playlistsの中から更新するテーブルを選択する
    
    for pl in playlists:
        if pl['name'] in update_table.keys():
            cur.execute("DROP TABLE IF EXISTS {};".format(update_table[pl['name']]))
            print("table droped: ", update_table[pl['name']])
            cur.execute("""
                CREATE TABLE IF NOT EXISTS {} (
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
            """.format(update_table[pl['name']]))
            print("create table: ", update_table[pl['name']])
            print('total tracks: ', pl['tracks']['total'])
            tracks = sp.playlist_tracks(pl['id'], fields="items.track.name, items.track.uri")
            #print(json.dumps(tracks, indent=4))

            for i, tr in enumerate(tracks['items']):
                track = tr['track']
                #print(json.dumps(sp.audio_features(track['uri']), indent=4))
                cur.execute("SELECT COUNT(index) FROM {};".format(update_table[pl['name']])) # primary_key(index)をあわせるためにcountしておく
                (cur_index, ) = cur.fetchone() # cur_indexはcurrent_index
                
                df = pd.DataFrame.from_dict(sp.audio_features(track['uri']))
                df = df.drop(labels=['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
                df.insert(loc=0, column='index', value=cur_index+1)
                df.insert(loc=1, column='name', value=track['name'])
                df.insert(loc=2, column='uri', value=track['uri'])

                print(df)
                df.to_csv('csv/{}.csv'.format(update_table[pl['name']]), header=False, index=False, encoding='utf-8')
                csv_file = open('csv/{}.csv'.format(update_table[pl['name']]), mode='r', encoding='utf-8')
                cur.copy_expert("COPY {} FROM STDIN (FORMAT CSV, ENCODING 'UTF8');".format(update_table[pl['name']]), csv_file)
                csv_file.close()
    conn.commit()
    cur.close()
    conn.close()