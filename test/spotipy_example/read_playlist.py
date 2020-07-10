from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlist_id = 'spotify:user:spotifycharts:playlist:37i9dQZEVXbJiZcmkrIHGU'
#playlist_id = 'spotify:playlist:5RIbzhG2QqdkaP24iXLnZX' # Resident Archive

results = sp.playlist(playlist_id)
print(json.dumps(results, indent=4))