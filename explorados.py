# -*- coding: utf-8 -*-

import ldap
import atexit
import os
import sys
import getpass
import struct

# To find out the logon server, run, on Windows,
# in command prompt (cmd.exe):
#  echo %LOGONSERVER%
#  echo %USERDNSDOMAIN%

SERVER = ''
DOMAIN = ''

DOMAIN = DOMAIN.lower()
base = 'dc='+',dc='.join(DOMAIN.split('.'))

user = ''
cont = 3
while (not user) and (cont > 0):
    user = input('Username: ')
    cont -= 1

if not user: sys.exit(1)

password = getpass.getpass()

try:
    # Secure LDAP connection: https://stackoverflow.com/questions/7716562/pythonldapssl
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    l = ldap.initialize('ldaps://{}'.format(SERVER))
    l.set_option(ldap.OPT_REFERRALS, 0)
    l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
    l.set_option( ldap.OPT_X_TLS_DEMAND, True )
    l.set_option( ldap.OPT_DEBUG_LEVEL, 255 )
    bind = l.simple_bind_s(user+"@"+DOMAIN, password)
    atexit.register(lambda: l.unbind())

except:
    print('Sorry, we\'ve got some problem.')

# Function copied from:
# https://stackoverflow.com/questions/33188413/python-code-to-convert-from-objectsid-to-sid-representation
def convert_sid(binary):
    version = struct.unpack('B', binary[0])[0]
    # I do not know how to treat version != 1 (it does not exist yet)
    assert version == 1, version
    length = struct.unpack('B', binary[1])[0]
    authority = struct.unpack('>Q', '\x00\x00' + binary[2:8])[0]
    string = 'S-%d-%d' % (version, authority)
    binary = binary[8:]
    assert len(binary) == 4 * length
    for i in xrange(length):
        value = struct.unpack('<L', binary[4*i:4*(i+1)])[0]
        string += '-%d' % (value)
    return string

def query_account(acct_name):
   criteria = "(&(objectClass=user)(sAMAccountName={}))".format(acct_name)
   attributes = None
   result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)

   results = [entry for dn, entry in result if isinstance(entry, dict)]
   data = results[0] if len(results) == 1 else {}
   return data


def query_groups(acct_name):
   criteria = "(&(objectClass=user)(sAMAccountName={}))".format(acct_name)
   attributes = ['memberOf']
   result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)

   results = [entry for dn, entry in result if isinstance(entry, dict)]
   data = results[0] if len(results) == 1 else {}
   dn_groups = data['memberOf']
   groups = []
   for dn_g in dn_groups:
      group_name = dn_g.split(',')[0].split('=')[1].lower()
      if not ' ' in group_name:
         groups.append(group_name)

   return groups
