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

    playlists = sp.current_user_playlists()['items'] # => random_selected
    user_id = sp.me()['id'] # 自分のspotify上のIDが出る
    update_table = ['random_selected']

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
                (cur_index, ) = cur.fetchone()
                df = pd.DataFrame.from_dict(sp.audio_features(track['uri']))
                df = df.drop(labels=['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms'], axis=1)
                df.insert(loc=0, column='index', value=cur_index+1)
                df.insert(loc=1, column='name', value=track['name'])
                df.insert(loc=2, column='uri', value=track['uri'])
                #print(df)
                df.to_csv('csv/random_features.csv', header=False, index=False)
                csv_file = open('csv/random_features.csv', mode='r', encoding='utf-8')
                cur.copy_from(csv_file, 'random_selected', sep=',')
                csv_file.close()

    conn.commit()
    cur.close()
    conn.close()