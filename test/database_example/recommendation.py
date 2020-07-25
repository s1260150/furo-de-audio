# random_selected tableから特徴量を選択し、作ったmodelをつかって特徴量間の距離を求める。
# kmeansは距離ベース, GMMは尤度でレコメンドする曲を選択する
# この手法はもう少し工夫する必要がある。GMMsの選曲は対数尤度ではなく、random_samplingでもいいかもしれない=>こちらのほうがレコメンドとして自然かもしれない
# 次にやること。。。協調フィルタリングを使ってレコメンド、unpersonalizedのレコメンドをする

# library for database
import psycopg2 as pg2
# library for recommendation
import numpy as np
from sklearn.externals import joblib

def compute_min_cost_kmeans(centroid, features):
    min_cost, min_index = None, None
    for i, mfcc in enumerate(features):
        cost = 0
        for c in centroid:
            #print(type(c), c)
            cost = cost + np.sum(np.abs(c - mfcc))
        if min_cost is None or cost < min_cost:
            min_cost, min_index = cost, i
    return min_index

def compute_min_cost_gmms(model, features):
    min_cost, min_index = None, None
    for i, mfcc in enumerate(features):
        cost = model.score(mfcc.reshape(1, -1)) #曲の対数尤度をもとめる
        if min_cost is None or cost < min_cost:
            min_cost, min_index = cost, i
    return min_index

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
    
    users = ['r', 'y']
    refer_table = ['random_selected'] # これらのtableをもとにrecommendしていく
    recommend_table = ['recommended_r', 'recommended_y']
    
    cursor.execute("SELECT acousticness, danceability, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, time_signature, valence FROM random_selected;")
    features = cursor.fetchall()
    features = np.array(features)

    for i, reco_table in enumerate(recommend_table):
        kmeans_ = joblib.load("model/kmeans_recommend_"+users[i]+".pkl")
        gmms_ = joblib.load("model/gmms_recommend_"+users[i]+".pkl")
        models = [kmeans_, gmms_]
        for model in models:
            cursor.execute("SELECT COUNT(index) FROM {};".format(reco_table)) # primary_key(index)をあわせるためにcountしておく
            (cur_index, ) = cursor.fetchone()
            min_cost, min_index = None, None
            if model is kmeans_:
                min_index = compute_min_cost_kmeans(model.cluster_centers_, features)
            else:
                min_index = compute_min_cost_gmms(model, features)
            
            print(min_index)
            cursor.execute("SELECT index, name, uri FROM random_selected where index = {0};".format(min_index))
            record = cursor.fetchall()
            print(record)
            cursor.execute("INSERT INTO {0} (index, name, uri, evaluation) VALUES ({1}, '{2}', '{3}', 0);".format(reco_table, cur_index, record[0][1], record[0][2]))
    conn.commit()
    cursor.close()
    conn.close()