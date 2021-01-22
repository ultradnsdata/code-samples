# some python tools

Uses python3.

* requirements.txt - contains the necessary python modules
```pip install -r requirements.txt```

* exploreultradata.py

```
usage: exploreultradata.py [-h] [-u username] [-p password] [-c command] domlist

positional arguments:
  domlist               file containing a list of domains to check, one domain per line (max 25 rows)
 
optional arguments:
  -h, --help            show this help message and exit
  -u username, --user username
  -p password, --pwd password
  -c command, --cmd command
                        one of [hostips, subdomains, nameservers]. defaults to hostips

```
