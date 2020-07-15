import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import os
import pandas as pd
import pprint

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(os.environ.get('SPOTIPY_CLENT_ID'), os.environ.get('SPOTIPY_CLIEND_SECRET'))
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# PandasでCSVを読み込む、最初の行は省略
songs = pd.read_csv("./sampleData/regional-jp-daily-latest.csv", index_col=0, header=1)
# インデックスをリセットし、振り直す 0-index
songs = songs.reset_index()
#print(songs.head(10))
#[position, track_name, artist, stream, url]

# PandasのDataFrame作成
song_info = pd.DataFrame()

# 楽曲数分の情報を取得
for url in songs["URL"]: 
    df = pd.DataFrame.from_dict(spotify.audio_features(url))
    song_info = song_info.append(df)
#print(song_info.head(10)) このままだと0のindexがそのまま追加されている

# song_infoのインデックスを振り直す
song_info = song_info.reset_index(drop=True)#drop=Trueでもとのindexをdrop
#print(song_info.head(10))
#[acousticness, analysis_url, danceability, duration_ms, energy, id, instrumentalness, key, liveness, loudness]

feature_table = pd.concat([songs, song_info], axis=1).to_csv("./sampleData/songs.csv")