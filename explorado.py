#!/usr/bin/python
# -*- coding: utf-8 -*-

import ldap
import atexit
import os
import sys
import getpass

# Para descobrir o nome de seu servidor, execute, no Windows, 
# via Prompt do DOS (cmd.exe): 
#  echo %LOGONSERVER%
#  echo %USERDNSDOMAIN%

SERVIDOR = ''
DOMINIO = ''

DOMINIO = DOMINIO.lower()
base = 'dc='+',dc='.join(DOMINIO.split('.'))

usuario = ''
cont = 3
while (not usuario) and (cont > 0):
    usuario = raw_input('Usuário: ')
    cont -= 1

if not usuario: sys.exit(1)

senha = getpass.getpass()

l = ldap.initialize(servidor)
try:
   l.protocol_version = ldap.VERSION3
   l.set_option(ldap.OPT_REFERRALS, 0)
   bind = l.simple_bind_s(usuario+"@"+DOMINIO, senha)
   atexit.register(lambda: l.unbind())

except:
   print('Sinto muito, aconteceu algum problema.')

def consulta_dados(conta):
   criteria = "(&(objectClass=user)(sAMAccountName={}))".format(conta)
   attributes = None
   result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
   results = [entry for dn, entry in result if isinstance(entry, dict)]
   dados = results[0] if len(results) == 1 else {}
   return dados


def consulta_grupos(conta):
   criteria = "(&(objectClass=user)(sAMAccountName={}))".format(conta)
   attributes = ['memberOf']
   result = l.search_s(base, ldap.SCOPE_SUBTREE, criteria, attributes)
 
   results = [entry for dn, entry in result if isinstance(entry, dict)]
   dados = results[0] if len(results) == 1 else {}
   dn_grupos = dados['memberOf'] 
   grupos = []
   for dn_g in dn_grupos:
      nome_grupo = dn_g.split(',')[0].split('=')[1].lower()
      if not ' ' in nome_grupo:
         grupos.append(nome_grupo)
   
   return grupos
