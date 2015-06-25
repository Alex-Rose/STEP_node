import argparse
import urllib
from pymongo import MongoClient
from auth import Auth

user = None
home = None
desc = None
web  = None
port = None
admin = None
email = None
interactive = False

parser = argparse.ArgumentParser()

parser.add_argument('-u', '--user',
    action="store", dest="user",
    help="unix username", required=True)

parser.add_argument('-d', '--home',
    action="store", dest="home",
    help="unix home location without trailing slash")

parser.add_argument('-D', '--desc',
    action="store", dest="desc",
    help="account description")

parser.add_argument('-w', '--web',
    action="store", dest="web",
    help="web address for hosting")

parser.add_argument('-p', '--port',
    action="store", dest="port",
    help="port to forward traffic to")

parser.add_argument('-a', '--admin',
    action="store", dest="admin",
    help="administrator name")

parser.add_argument('-e', '--email',
    action="store", dest="email",
    help="administrator email")

parser.add_argument('-i', '--interactive',
    action="store_true", dest="interactive",
    help="enable interactive mode")


args = parser.parse_args()

print 'args', args

def interactive():
	if home is None:
		home = raw_input('Home dir for user : ')
	
	if home is None:
                desc = raw_input('Description : ')

	if home is None:
                web = raw_input('Web address : ')

	if home is None:
                port = raw_input('Listening port : ')

	if home is None:
                admin = raw_input('Administrator name : ')

	if home is None:
                email = raw_input('Administrator email : ')


if interactive:
	interactive()


username = Auth.username
password = urllib.quote_plus(Auth.password)

string = 'mongodb//'+username+':'+password+'@127.0.0.1:27017'

c = MongoClient()
c.admin.authenticate(Auth.username, Auth.password)

users = c.admin_step.users.find({"web":{'$exists': True}})
for user in users:
        #print user['web']['home']
	for web in user['web']:
#		script = web['home'] + '/.web_init.sh'
		print web



