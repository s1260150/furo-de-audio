import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import os
import pprint

CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

name = 'Nogizaka46'

#乃木坂46の情報をゲットする
nogi_uri = spotify.search(q='artist:' + name, type='artist')['artists']['items'][0]['uri']
print("Nogizaka46's uri: ", nogi_uri) #=> spotify:artist:08lN7bm4Etec8ETFxaTUmq

#result = spotify.search("08lN7bm4Etec8ETFxaTUmq")
#pprint.pprint(result)

"""
print(spotify.artist(nogi_uri)) # return dictionary
#spotify.artist(nogi_uri)["external_urls"] =>ブラウザから検索できるURL
#spotify.artist(nogi_uri)["genres"]        =>アーティストのジャンル　複数存在可能
#spotify.artist(nogi_uri)["id"]            =>アーティストのid  
#spotify.artist(nogi_uri)["images"]        =>検索したときのトップ画像
#spotify.artist(nogi_uri)["name"]          =>アーティストの名前
#spotify.artist(nogi_uri)["popularity"]    =>アーティストの人気度 0~100で100に近づくほど人気
#spotify.artist(nogi_uri)["type"]          =>アーティストのtype? artistと出る
#spotify.artist(nogi_uri)["uri"]           =>spotify:artist:idの形

related_artist = []
for artist in spotify.artist_related_artists(nogi_uri)['artists']:
    related_artist.append([artist['name'], artist['uri'].split(':')[2]])
    print(artist['name'])
"""