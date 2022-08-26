# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

from playlist_model import PlaylistModel

scope = "user-library-read, playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


def get_current_user_id():
    results = sp.current_user()
    # pprint(results)
    return results['id']


def get_artist_album(id):
    founded_array = []
    artist_album_response = sp.artist_albums(id, limit=50)
    # print(artist_album_response)
    for idx, item in enumerate(artist_album_response['items']):
        founded_array.append({
            'id': item['id'],
            'uri': item['uri'],
            'name': item['name'],
            'release_date': item['release_date'],
            'total-total_tracks': item['total_tracks'],
        })
    return founded_array


def search_artist(artistName):
    founded_array = []
    founded_itens = sp.search(artistName, 10, 0, 'artist')
    for i, fitem in enumerate(founded_itens['artists']['items']):
        founded_array.append({
            'id': fitem['id'],
            'uri': fitem['uri'],
            'name': fitem['name'],
            'total-followers': fitem['followers']['total'],
        })
        # print(fitem['id'] + ' - ' + fitem['uri'] + ' - '+fitem['name']+' - '+str(fitem['followers']['total']))
        return founded_array


def list_recents_tracks():
    results = sp.current_user_saved_tracks()
    for idx, item in enumerate(results['items']):
        track = item['track']
        print(idx, track['artists'][0]['name'], " – ", track['name'])


def get_tracks_from_album(id):
    founded_array = []
    response_tracks = sp.album_tracks(id)
    for idx, item in enumerate(response_tracks['items']):
        founded_array.append({
            'id': item['id'],
            'uri': item['uri'],
            'name': item['name']
        })
    return founded_array

def print_hi(name):
    collection = list_all_my_playlists()
    has_temp_playlist = False
    tmp_playlist: PlaylistModel
    for playlistModel in collection:
        print(playlistModel)
        if playlistModel.name == 'GENERATED_PLAYLIST':
            has_temp_playlist = True
            tmp_playlist = playlistModel
            print('Usando existente')
            break
    if not has_temp_playlist:
        print('Criando uma nova')
        tmp_playlist = create_tmp_playlist()
    print(tmp_playlist)


def list_all_my_playlists():
    offset = 0
    limit = 50
    itens = limit
    collection_playlist = []
    while (itens - limit) >= 0:
        itens, collection_playlist_tmp = list_my_playlists(limit, offset)
        offset = offset + itens
        collection_playlist.extend(collection_playlist_tmp)
    return collection_playlist


def create_tmp_playlist():
    response = sp.user_playlist_create(
        get_current_user_id(),
        'GENERATED_PLAYLIST',
        False,
        False,
        'GENERATED_PLAYLIST_BY_PYTHON'
    )
    return PlaylistModel(response['id'], response['name'], response['uri'], response['tracks']['total'])


def list_my_playlists(limit=50, offset=0):
    playlists = sp.current_user_playlists(limit, offset)
    count = 0
    collection_playlist = []
    for i, playlist in enumerate(playlists['items']):
        name = playlist['name']
        _id = playlist['id']
        uri = playlist['uri']
        _size = playlist['tracks']['total']
        playlist_model = PlaylistModel(_id, name, uri, _size)
        collection_playlist.append(playlist_model)
        # print(playlist_model)
        count = count + 1
    return count, collection_playlist


if __name__ == '__main__':
    # print_hi('PyCharm')
    results = search_artist('Iron Maiden')
    main_result = results[0]
    albuns = get_artist_album(main_result['id'])
    get_tracks_from_album(albuns[0]['id'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
