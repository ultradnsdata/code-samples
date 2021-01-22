import json
from datetime import date, timedelta
import calendar
import argparse
import csv
import time
from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session

authToken = None


def build_arg_parser():
  parser = argparse.ArgumentParser(description="Explore UltraData API")
  parser.add_argument('-u', '--user', metavar='username', default='udataapi', help='')
  parser.add_argument('-p', '--pwd', metavar='password', default='')
  parser.add_argument('-c', '--cmd', metavar='command', help='one of [hostips, subdomains, nameservers]. defaults to hostips', default='hostips')
  parser.add_argument('domlist', help='file containing a list of domains to check, one domain per line (max 25 rows)')
  return parser


def query(clnt, url, hdr, params=None):
  req = clnt.get(url, params=params, headers=hdr)
  d = req.json()
  if req.status_code == 202 and 'location' in d and 'poll-interval-s' in d:
    time.sleep(int(d['poll-interval-s']))
    return query(clnt, d['location'], hdr)
  else:
    return d


def save_token(newtoken):
    authToken = newtoken


if __name__ == '__main__':
  p = build_arg_parser()
  client_id = 'ultradataexplorer'
  
  base_url = 'https://api.ultradata.neustar/v1'
  oauth = None
  domcnt = 0
  header = {'Accept': '*/*'}

  token_url = '{}/authorization/token'.format(base_url)
  cmdmap = {'hostips':'{}/domain/hostips'.format(base_url),
            'subdomains':'{}/domain/subdomains'.format(base_url),
            'nameservers':'{}/domain/domainnameservers'.format(base_url)}

  endtime = calendar.timegm(date.today().timetuple())
  starttime = endtime - int(timedelta(days=7).total_seconds())

  params = {'domain': '', 'starttime': starttime, 'endtime': endtime}

  try:
    opts = p.parse_args()
  except IOError as e:
    p.print_help()
    sys.exit(2)

  if opts.cmd not in cmdmap:
    p.print_help()
    sys.exit(2)

  # set up oauth token
  oauth = OAuth2Session(client=LegacyApplicationClient(client_id=client_id))
  authToken = oauth.fetch_token(token_url=token_url,
                            username=opts.user,
                            password=opts.pwd)

  # initiate a client session to auto refresh the token
  client = OAuth2Session(client_id,
                         token=authToken,
                         auto_refresh_url=token_url,
                         token_updater=save_token)

  with open(opts.domlist) as f:
    cr = csv.reader(f)
    for r in cr:
      if len(r) >= 1 and domcnt < 25:
        domcnt += 1
        params['domain'] = r[0]
        result = query(client, cmdmap[opts.cmd], header, params)
        print ('\n\t***\t{}\t***'.format(r[0]))
        print ('\t***\t{}\t***'.format(cmdmap[opts.cmd]))
        print (json.dumps(result, indent=2))
