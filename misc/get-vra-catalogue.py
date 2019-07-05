#!/usr/bin/env python

"""
    Retrieves vRealize entitled catalog items that match the value passed into '-n'

    based on https://github.com/kovarus/vrealize-pysdk/blob/master/get-catalog.py
"""

# TODO set an environment variable that stores the auth token
# TODO create a check for auth token env variable. If present don't prompt for password

__version__ = "$Revision$"
# $Source$

import getpass
import argparse
import vralib
from prettytable import PrettyTable
import os

def getargs():
  parser = argparse.ArgumentParser()
  parser.add_argument('-s', '--server',
                      required=False,
                      action='store',
                      default='vra.wehi.edu.au',
                      help='FQDN of the Cloud Provider.')
  parser.add_argument('-u', '--username',
                      required=False,
                      action='store',
                      default=os.getenv('USER'),
                      help='Username to access the cloud provider')
  parser.add_argument('-t', '--tenant',
                      required=False,
                      action='store',
                      default='Milton',
                      help='vRealize tenant')
  return parser.parse_args()

def main():

  args = getargs()
  cloudurl = args.server
  username = args.username
  tenant = args.tenant

  if not username:
      username = input("vRA Username (user@domain):")

  password = getpass.getpass("vRA Password:")

  vra = vralib.Session.login(username, password, cloudurl, tenant, ssl_verify=False)

  catalog = vra.get_entitled_catalog_items()

  out = PrettyTable(['Name', 'Description'])
  out.align['Name'] = 'l'
  out.padding_width = 1
  for i in catalog['content']:
    c = i['catalogItem']
    out.add_row((c['name'], c['description']))
  print(out)

if __name__ == '__main__':
  main()