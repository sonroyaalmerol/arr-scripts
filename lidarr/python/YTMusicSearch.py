from ytmusicapi import YTMusic
import sys
import json

def search_artist(query):
    yt = YTMusic()
    search_results = yt.search(
        query=query,
        filter='artists',
        limit=1,
    )

    if len(search_results) == 0:
        print('-1')
        return
    
    result = search_results[0]
    print(result['browseId'])

def get_artist_albums(artist_id):
    yt = YTMusic()
    albums = yt.get_artist_albums(artist_id)
    detailed_albums = []

    for album in albums:
        details = yt.get_album(album['browseId'])
        details['browseId'] = album['browseId']
        detailed_albums.append(details)

    json_string = json.dumps(detailed_albums)
    print(json_string)

if __name__ == '__main__':
    # Check if any arguments were provided
    if len(sys.argv) < 3:
        print("Not enough arguments provided.")
        sys.exit(1)
    else:
        query_type = sys.argv[1]
        query = sys.argv[2]

        if query_type == 'artist-albums':
            get_artist_albums(query)
            sys.exit()

        if query_type == 'artists':
            search_artist(query)
            sys.exit()