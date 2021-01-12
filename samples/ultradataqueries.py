#!/usr/bin/python3

import sys
import requests
from time import sleep
from datetime import *
from dateutil.relativedelta import *

import ultradatagettoken

def ultradata_api(token,function,params):
    response_code = requests.codes.accepted
    while response_code == requests.codes.accepted:
        print('Requesting %s'%(function))
        activity_response = requests.get(URL+function,
                                         #allow_redirects=False,
                                         params=params,
                                         headers={
                                             'Authorization': 'Bearer '+token
                                         })
        response_code = activity_response.status_code
        if response_code == requests.codes.accepted:
            print('Received a 202 for domain/activity.  Have to wait and try again')
            sleep(activity_response.json()['poll-interval-s'])


    if activity_response.status_code == requests.codes.ok:
        print(activity_response.json())
    else:
        print('Response code: %s'%(activity_response.status_code))
        print()
        print(activity_response.json())

if __name__ == '__main__':
    URL='https://api.ultradata.neustar/v1'
    NOW=datetime.now()
    STARTTIME=int((NOW+relativedelta(days=-6)).timestamp())
    ENDTIME=int((NOW+relativedelta(days=-2)).timestamp())
    try:
        token = ultradatagettoken.ultradata_login()
    except Exception as e:
        print('Login failure')
        sys.exit(1)

    for function in [
            "/domain/activity",
            "/domain/hostips",
            "/domain/subdomains",
            "/domain/zonedomains", #will return an empty set: neustar.biz is not a ns name like pdns196.ultradns.biz
            "/domain/domainnameservers",
            "/domain/extra"]:
        
        ultradata_api(token,function,{
            'domain': 'neustar.biz',
            'starttime': STARTTIME,
            'endtime': ENDTIME
        })
    print()
    ultradata_api(token,"/address/hostdomainnames",{
        'cidr': '156.154.240.232-32',
        'starttime': STARTTIME,
        'endtime': ENDTIME
    })
    ultradata_api(token,"/address/netactivity",{
        'cidr': '156.154.240.232-32',
        'starttime': STARTTIME,
        'endtime': ENDTIME
    })

