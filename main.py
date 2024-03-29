from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="user-library-read playlist-read-private playlist-modify-private playlist-modify-public",
#       The scope in line 8 defines what permissions you are enabling, such as allowing the script to read your playlists and modify/update if chosen
        redirect_uri="http://example.com",
        client_id=os.environ["CLIENT_ID"],
        client_secret=os.environ["CLIENT_SECRET"],
        show_dialog=True,
        cache_path="token.txt"))
user_id = sp.current_user()["id"]
playlists = sp.current_user_playlists()['items']
results = sp.current_user_saved_tracks(limit=50, offset=0, market='US')
saved_songs = results['items']
while results['next']:
    results = sp.next(results)
    saved_songs.extend(results['items'])
tracks = [x['track'] for x in saved_songs]
songs = [x['name'] for x in tracks]
song_ids = [x['id'] for x in tracks]
for x in playlists:
#     This checks all of your spotify playlist names and introduces the condition to delete a specific playlist if the name "Liked Songs" is matched. 
#     It only applies if this script was run multiple times. It is used as a way to update the playlist or in other words delete the old and create the new. 
    if x['name']== "Liked Songs":
        playlist = x
        for i in range(0, len(saved_songs), 100):
            sp.current_user_unfollow_playlist(playlist_id=playlist['id'])
        print("Playlist Deleted")
        break
else:
    public_or_private = input("Do you want the playlist to be public? True or False: ").capitalize()
    playlist = sp.user_playlist_create(user=user_id, name="Liked Songs", public=public_or_private)
    for i in range(0, len(saved_songs), 100):
        sp.playlist_add_items(playlist_id=playlist['id'], items=song_ids[i:i + 100])
#       This step will add all of your saved songs into the new playlist, in this case it is called "Liked Songs."
