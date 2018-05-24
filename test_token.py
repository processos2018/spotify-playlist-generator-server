import spotipy
import spotipy.util as util

from src import Token

if Token.query.count() > 0:
    token = Token.query.get(1)

    spotipy_ = spotipy.Spotify(auth=token.token_value)

    results = spotipy_.search(q='artist:' + 'Bruno Mars', type='artist')
    print(results)
