import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from client_id import *
import sys

client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(CLIEND_ID, CLIEND_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#LedZeppelin
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
results = spotify.artist_top_tracks(lz_uri)

for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()