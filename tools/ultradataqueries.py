#!/usr/bin/python3

import sys
import requests
from time import sleep
from datetime import *
from dateutil.relativedelta import *

import ultradatagettoken

if __name__ == '__main__':
    URL='https://api.miranda.neustar/v1'
    NOW=datetime.now()
    STARTTIME=int((NOW+relativedelta(days=-4)).timestamp())
    ENDTIME=int((NOW+relativedelta(days=-2)).timestamp())
    try:
        token = ultradatagettoken.ultradata_login()
    except Exception as e:
        print('Login failure')
        sys.exit(1)

    response_code = requests.codes.accepted
    while response_code == requests.codes.accepted:
        print('Requesting domain/activity')
        activity_response = requests.get(URL+"/domain/activity",
                                         #allow_redirects=False,
                                         params={
                                             'domain': 'neustar.biz',
                                             'starttime': STARTTIME,
                                             'endtime': ENDTIME
                                         },
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

    print()
