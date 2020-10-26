import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
import pandas as pd

# Get the username from terminal
username = sys.argv[1]

scope = 'playlist-read-private'
client_id = 'fde49ceea07644e0be10b8b8a00fd219'
client_secret = '05c59788f3f144c7a74fac51ac2b3f7b'
redirect_uri = 'http://www.google.com/'

# Username: 22xfmjx4dkqmlx5xiy3zndtlq & 125733088

#Erase cache and prompt for user permission
try:
	token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
except:
	os.remove(f'.cache-{username}')
	token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

# create our spotifyObject

spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()

displayName = user['display_name']
followers = user['followers']['total']

while True:

	print()
	print(">>> Welcome to Spotipy, " + displayName + "!")
	print(">>> You have " + str(followers) + " followers.")
	print()
	print("0 - Search for an artist")
	print("1 - Playlist Analysis")
	print("2 - Exit")
	print()
	choice = input("Your choice: ")
	print()

	# Search for artist
	if choice == "0":
		print()
		searchQuery = input("Okay, what is the artist name?: ")
		print()

		#Get search result
		searchResults = spotifyObject.search(searchQuery,1,0,"artist")
		#print(json.dumps(searchResults, sort_keys=True, indent=4))

		# Artist Details
		artist = searchResults['artists']['items'][0]
		artistID = artist['id']
		print()
		print("Name: " + artist['name'])
		print("Popularity: " + str(artist['popularity']))
		print("Followers: " + str(artist['followers']['total']))
		print("Genre: " + artist['genres'][0])
		print()
		webbrowser.open(artist['images'][0]['url'])

		# Album and track Details
		trackURIs = []
		trackArt = []
		z = 0

		# Extract album data
		albumResults = spotifyObject.artist_albums(artistID)
		albumResults = albumResults['items']

		for item in albumResults:
			print("ALBUM: " + item['name'])
			albumID = item['id']
			albumArt = item['images'][0]['url']

			#Extract track data
			trackResults = spotifyObject.album_tracks(albumID)
			trackResults = trackResults['items']

			for item in trackResults:
				print(str(z) + ": " + item['name'])
				trackURIs.append(item['uri'])
				trackArt.append(albumArt)
				z+=1
			print()
		
		# See album art
		while True:
			songSelection = input("Enter a song to see the album art associated with it (x to exit): ")
			if songSelection == "x":
				break
			webbrowser.open(trackArt[int(songSelection)])

	if choice =="1":
		print()
		searchQuery = input("Okay, what is the playlist ID?: ") #2rZBaQnLJIZDqTTXmckD4p #h6YI3rDz0IFDkL7ASAF4cuI
		print()

		# Get search result
		searchResults = spotifyObject.user_playlist(user='22xfmjx4dkqmlx5xiy3zndtlq', playlist_id=searchQuery)
		#print(json.dumps(searchResults, sort_keys=True, indent=4))

		# Get Playlist elements
		def getTrackIDs(user1, playlist_id1):
			ids=[]
			playlist = spotifyObject.user_playlist(user='22xfmjx4dkqmlx5xiy3zndtlq', playlist_id=searchQuery)
			for item in playlist['tracks']['items']:
				track = item['track']
				ids.append(track['id'])
			return ids

		ids = getTrackIDs(user, searchQuery)
		#print(ids)

		def getTrackFeatures(id):
			meta=spotifyObject.track(id)
			features = spotifyObject.audio_features(id)

			# meta
			name=meta['name']
			album = meta['album']['name']
			artist = meta['album']['artists'][0]['name']
			release_date = meta['album']['release_date']
			length = meta['duration_ms']
			popularity = meta['popularity']

			# features	
			acousticness = features[0]['acousticness']
			danceability = features[0]['danceability']
			energy = features[0]['energy']
			instrumentalness = features[0]['instrumentalness']
			liveness = features[0]['liveness']
			loudness = features[0]['loudness']
			speechiness = features[0]['speechiness']
			tempo = features[0]['tempo']
			time_signature = features[0]['time_signature']

			track = [name, album, artist, release_date, length, popularity, danceability, acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
			return track

		# loop over track ids 
		tracks = []
		for i in range(len(ids)):
		    #time.sleep(.5)
		    track = getTrackFeatures(ids[i])
		    tracks.append(track)

		df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
		print(df)
		print()
		df.to_csv("playlist_analysis.csv", sep = ',')
		print("Data has been export data to excel.")
		print()


	# End of program	
	if choice == "2":
		print()
		print("Goodbye, sucker.")
		print()
		break



# print(json.dumps(VARIABLE, sort_keys=True, indent=4))
