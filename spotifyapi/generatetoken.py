from requester import Requester
import sys

user_id = None
client_id = None
secret = None
redirect_uri = None

if len(sys.argv) > 1:
    user_id = sys.argv[1]

if len(sys.argv) > 2:
    client_id = sys.argv[2]

if len(sys.argv) > 3:
    secret = sys.argv[3]

if len(sys.argv) > 4:
    redirect_uri = sys.argv[4]

requester = Requester()
requester.getToken(user_id, client_id, secret, redirect_uri)
