import spotipy
import spotipy.util as util

class Requester(object):
    def search(self, artist):
        token = util.prompt_for_user_token('i5ou0pbtla8uutgmndo5gz52v', redirect_uri = '')

        spotipy_ = spotipy.Spotify(auth=token)

        results = spotipy_.search(q='artist:' + artist, type='artist')
        print(results)
