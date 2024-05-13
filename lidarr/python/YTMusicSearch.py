from ytmusicapi import YTMusic
from countryinfo import CountryInfo
import sys
import json

supported_languages = [
    'ar', 'de', 'es', 'en', 'fr', 'hi',
    'it', 'ja', 'ko', 'nl', 'pt',
    'ru', 'tr', 'ur', 'zh_CN', 'zh_TW'
]

def get_languages(country):
    if country == None:
        return ['en']
        
    country = country.lower()

    country_data = CountryInfo(country)
    languages = country_data.languages()
    
    try:
        zh_index = languages.index('zh')
    except ValueError:
        zh_index = -1
    
    if zh_index != -1:
        if country == 'tw':
            languages[zh_index] = 'zh_TW'
        else:
            languages[zh_index] = 'zh_CN'

    result = list(filter(lambda x: x in supported_languages, languages))
    
    if len(result) == 0:
        result = ['en']

    # Ignore other languages if English is one of the official languages
    if len(list(filter(lambda x: x == 'en', result))) != 0:
        result = ['en']
    
    return result

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

def search_music(query, country=None):
    langs = get_languages(country)

    search_results = []
    for lang in langs:
        yt = YTMusic(language=lang)
        search_results = search_results + yt.search(
            query=query,
            filter='songs',
        )
        
    json_string = json.dumps(search_results)
    print(json_string)

def get_artist_albums(artist_id, country=None):
    langs = get_languages(country)

    detailed_albums = []

    for lang in langs:
        yt = YTMusic(language=lang)
        artist = yt.get_artist(artist_id)

        if 'albums' in artist:
            if 'results' in artist['albums']:
                for album in artist['albums']['results']:
                    details = yt.get_album(album['browseId'])
                    details['browseId'] = album['browseId']
                    detailed_albums.append(details)
        
        if 'singles' in artist:
            if 'results' in artist['singles']:
                for single in artist['singles']['results']:
                    details = yt.get_album(single['browseId'])
                    details['browseId'] = single['browseId']
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

        if len(sys.argv) > 3:
            country = sys.argv[3]
        else:
            country = None

        if query_type == 'artist-albums':
            get_artist_albums(query, country)
            sys.exit()

        if query_type == 'artists':
            search_artist(query)
            sys.exit()

        if query_type == 'songs':
            search_music(query, country)
            sys.exit()