import spotipy
import json
from dotenv import dotenv_values

config = dotenv_values(".env")

# get from spotify dashboard
SPOTIPY_CLIENT_ID = config['SPOTIPY_CLIENT_ID']
# get from spotify dashboard
SPOTIPY_CLIENT_SECRET = config['SPOTIPY_CLIENT_SECRET']
# get from spotify dashboard
USERNAME = config['USERNAME']
# set this in spotify dashboard
REDIRECT_URI = config['REDIRECT_URI']
SCOPE = config['SCOPE']

DUMP_TO_JSON = True
DUMP_PLAYLIST_TO_JSON = "Spotify.json"
DUMP_PLAYLIST = "Ytdl.txt"

print("Initializing...")
print("Fetching token from Spotify")

token = spotipy.util.prompt_for_user_token(
    USERNAME, SCOPE, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, REDIRECT_URI)

print("Fetching token completed")

sp = spotipy.Spotify(token)

metaDetails = []


def grabMetadata(metaDetails, spotifyResults):
    print(f"Processed {len(metaDetails)} file for metadata")
    print("Processing results as batch")
    for item in spotifyResults['items']:

        songMetadata = {
            "artist": item['track']['artists'][0]['name'],
            "name": "",
            "uri": "",
            "duration_ms": "",
            "popularity": ""
        }

        for param in list(songMetadata.keys())[1:]:
            songMetadata[param] = item['track'][param]

        metaDetails.append(songMetadata)

    print("Processing results as batch completed")

    return metaDetails


# to fetch all liked songs
print("Fetching user's liked playlist")
spotifyResults = sp.current_user_saved_tracks()
print("Fetching user's liked playlist completed")

metaDetails = grabMetadata(metaDetails, spotifyResults)
while spotifyResults['next']:
    print("Fetching more from user's liked playlist")
    spotifyResults = sp.next(spotifyResults)
    print("Fetching more from user's liked playlist completed")
    metaDetails = grabMetadata(metaDetails, spotifyResults)

print(f"Fetched metadata from {len(metaDetails)} items(s)")
if DUMP_TO_JSON:
    print("Writing Spotify results to JSON")
    with open(DUMP_PLAYLIST_TO_JSON, 'w') as f:
        json.dump(metaDetails, f, indent="\t", sort_keys=False)
    print("Writing Spotify results to JSON completed")

with open(DUMP_PLAYLIST, 'w', encoding="utf8") as f:
    print("Dumpiing Spotify liked playlist to file")
    for item in metaDetails:
        f.write(f"{item['artist']} {item['name']}\n")
    print("Dumpiing Spotify liked playlist to file completed")

print(f"Successfully finished batch process. Invoke Downloader.")
