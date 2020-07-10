# insert tracks into playlist_r and playlist_y to update its content.
# insertと書いてはいるが、やっていることは基本的にspotifyから取ってきたプレイリスト情報を使ってtableの更新をすることである
# library for database
import psycopg2 as pg2
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
#from sklearn.mixture import GaussianMixtureModel
from sklearn.externals import joblib

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

    read_table = ['song_features_r', 'song_features_y']

    for i, table in enumerate(read_table):
        train_data = pd.DataFrame()
        cursor.execute("SELECT acousticness, danceability, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence FROM {};".format(table))
        result = cursor.fetchall()
        train_data = train_data.append(pd.DataFrame.from_records(result))
        print(train_data.head())
        
        kmeans_ = KMeans(n_clusters=3, random_state=None)
        kmeans_.fit(train_data)
        if table == 'song_features_r':
            joblib.dump(kmeans_, 'model/kmeans_recommend_r.pkl')
        else:
            joblib.dump(kmeans_, 'model/kmeans_recommend_y.pkl')

    conn.commit()
    cursor.close()
    conn.close()