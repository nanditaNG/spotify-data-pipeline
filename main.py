import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials

#setting up credentials
client_credentials_manager = SpotifyClientCredentials(client_id = "6f448a830e2c4c9bb888a33a177bcb8b", client_secret = "26d9570a64094f208f0393133b7be117")

#creating spotify object to extract data from Spotify API
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/5ABHKGoOzxkaa28ttQV9sE"

playlist_URI = playlist_link.split("/")[-1]

# print(playlist_URI)

data = sp.playlist_items(playlist_URI)

# print(data)

# print(data['items'][0]['track']['album']['id'])
#
# print(data['items'][0]['track']['album']['name'])
#
# print(data['items'][0]['track']['album']['release_date'])
#
# print(data['items'][0]['track']['album']['total_tracks'])
#
# print(data['items'][0]['track']['external_urls']['spotify'])

# for albums
album_list = []
for row in data['items']:
    album_id = row['track']['album']['id']
    album_name = row['track']['album']['name']
    album_release_date = row['track']['album']['release_date']
    album_total_tracks = row['track']['album']['total_tracks']
    album_URL = row['track']['album']['external_urls']['spotify']
    album_elements = {'album_id': album_id, 'album_name':album_name, 'release_date':album_release_date, 'album_total_tracks':album_total_tracks, 'album_URL': album_URL}
    album_list.append(album_elements)
# print(album_list)


# print(data['items'][0]['track']['artists'])

# for artist
artist_list = []
for row in data['items']:
    for key, value in row.items():
        if key == 'track':
            for artist in value['artists']:
                # print(artist)
                artist_elments = {'artist_id': artist['id'], 'artist_name': artist['name'], 'external_url': artist['href']}
                artist_list.append(artist_elments)
# print(artist_list)

# for tracks
track_list = []
# print(data['items'][0]['track'])

for row in data['items']:
    song_id = row['track']['id']
    song_name = row['track']['name']
    song_duration = row['track']['duration_ms']
    song_url = row['track']['external_urls']['spotify']
    song_popularity = row['track']['popularity']
    song_added = row['added_at']
    song_element = {'song_id':song_id, 'song_name': song_name, 'song_duration': song_duration, 'song_url': song_url, 'song_popularity': song_popularity, 'song_added': song_added}
track_list.append(song_element)



album_df = pd.DataFrame.from_dict(album_list)
album_df = album_df.drop_duplicates(subset = ['album_id'])

artist_df = pd.DataFrame.from_dict(artist_list)
artist_df = artist_df.drop_duplicates(subset = ['artist_id'])

track_df = pd.DataFrame.from_dict(track_list)
track_df = track_df.drop_duplicates(subset=['song_id'])


album_df['release_date'] = pd.to_datetime(album_df['release_date'], format='%Y-%m-%d', errors='coerce')
track_df['song_added']=pd.to_datetime(track_df['song_added'], format = '%Y-%m-%d', errors='coerce')

print(track_df['song_added'])

# extracted data using python, created trigger that will trigger lambda every one minute stores data in amazon s3
# extract data from spotify api and place that raw data in to_processed folder
# trigger whenever file is put onto the s3 bucket we trigeer the transformation function that puts data from respective transformation folder and moves data from to_proccesed to processed folder
