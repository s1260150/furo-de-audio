# insert tracks into playlist_r and playlist_y to update its content.
# insertと書いてはいるが、やっていることは基本的にspotifyから取ってきたプレイリスト情報を使ってtableの更新をすることである
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
# library for database
import psycopg2 as pg2
import pandas as pd
import numpy as np

#scope = 'playlist-modify-public'

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

    playlists = sp.current_user_playlists()['items'] # => myStreamR, myStreamY
    user_id = sp.me()['id'] # 自分のspotify上のIDが出る
    update_table = ['playlist_r', 'playlist_y']

    for i, pl in enumerate(playlists):
        if pl['name'] in update_table:
            print('total tracks before update: ', pl['tracks']['total'])
            tracks = sp.playlist_tracks(pl['id'], fields="items.track.name, items.track.uri")
            print(json.dumps(tracks, indent=4))

            cur.execute("SELECT COUNT(index) FROM {};".format(pl['name'])) # primary_key(index)をあわせるためにcountしておく
            (cur_index, ) = cur.fetchone() # cur_indexはcurrent_indexです

            df = pd.DataFrame.from_dict([tracks['items'][0]['track']])
            for j, tr in enumerate(tracks['items']):
                if j == 0: continue
                df = df.append([tr['track']])
            df.insert(loc=0, column='index', value=[cur_index+1+c for c in range(len(tracks['items']))])

            print(df.columns)
            df.to_csv('csv/{}.csv'.format(pl['name']), header=False, index=False)
            csv_file = open('csv/{}.csv'.format(pl['name']), mode='r', encoding='utf-8')
            #cur.copy_from(csv_file, pl['name'], sep=',')
            cur.copy_expert("COPY {} FROM STDIN (FORMAT CSV, ENCODING 'UTF8');".format(pl['name']), csv_file)
            csv_file.close()
    conn.commit()
    cur.close()
    conn.close()