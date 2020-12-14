#!/usr/bin/python
# -*- coding: utf-8 -*-

import ldap
import atexit
import os
import sys
import getpass
import struct

# Find out your logon server (LOGONSERVER) and DNS domain name (USERDNSDOMAIN).
# After that, replace the variables bellow accordinly.
# Commands to run on PowerShell (pwsh.exe): 
#  $env:LOGONSERVER
#  $env:USERDNSDOMAIN
#
# In case you prefer the command prompt (cmd.exe), run the commands: 
#  echo %LOGONSERVER%
#  echo %USERDNSDOMAIN%

SERVER = '' # The value of LOGONSERVER environment variable
DOMAIN = '' # The value of USERDNSDOMAIN environment variable

DOMAIN = DOMAIN.lower()
base = 'dc='+',dc='.join(DOMAIN.split('.'))


# Function copied from:
# https://stackoverflow.com/questions/33188413/python-code-to-convert-from-objectsid-to-sid-representation
def converte_sid(binary):
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

def consulta_conta(acct_name):
   criteria = f"(&(objectClass=user)(sAMAccountName={acct_name}))"
   attributes = None
   result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
   results = [entry for dn, entry in result if isinstance(entry, dict)]
   data = results[0] if len(results) == 1 else {}
   return data

def consulta_conta_por_email(mail_address):
   criteria = f"(&(objectClass=user)(mail={mail_address}))"
   attributes = None
   result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
   results = [entry for dn, entry in result if isinstance(entry, dict)]
   data = results[0] if len(results) == 1 else {}
   return data

def consulta_conta_por_email_escolar(mail_address):
   criteria = f"(&(objectClass=user)(extensionAttribute5={mail_address}))"
   attributes = None
   result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
   results = [entry for dn, entry in result if isinstance(entry, dict)]
   data = results[0] if len(results) == 1 else {}
   return data

def consulta_grupo(acct_name):
   criteria = f"(&(objectClass=user)(sAMAccountName={acct_name}))"
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

user = ''
cont = 3
while (not user) and (cont > 0):
    user = input('Matrícula: ')
    cont -= 1

if not user: sys.exit(1)

password = getpass.getpass()

l = ldap.initialize('ldap://{}'.format(SERVER))
try:
   l.protocol_version = ldap.VERSION3
   l.set_option(ldap.OPT_REFERRALS, 0)
   bind = l.simple_bind_s(user+"@"+DOMAIN, password)
   del password # To avoid memory leak
   atexit.register(lambda: l.unbind())

except:
   print('Sorry, we\'ve got some problems.')

meus_dados = consulta_conta(user)


