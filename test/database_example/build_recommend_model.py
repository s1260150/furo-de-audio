# library for database
import psycopg2 as pg2
# library for ai
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
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
        
        kmeans_ = KMeans(n_clusters=4, random_state=None)
        kmeans_.fit(train_data)
        gmms_ = GaussianMixture(n_components=4, covariance_type='diag', max_iter=200, random_state=None)
        gmms_.fit(train_data)
        if table == 'song_features_r':
            joblib.dump(kmeans_, 'model/kmeans_recommend_r.pkl')
            joblib.dump(gmms_, 'model/gmms_recommend_r.pkl')
        else:
            joblib.dump(kmeans_, 'model/kmeans_recommend_y.pkl')
            joblib.dump(gmms_, 'model/gmms_recommend_y.pkl')
    
    conn.commit()
    cursor.close()
    conn.close()