#!/usr/bin/python3
import requests
from pathlib import Path

def ultradata_login():

    with open(str(Path.home())+"/.ultradata/credentials", 'r') as file:
        data = file.readlines()
        for line in data:
            if line.startswith("ULTRA_USERNAME="):
                ULTRADATA_USERNAME=line[15:].strip()
            if line.startswith("ULTRA_PASSWORD="):
                ULTRADATA_PASSWORD=line[15:].strip()

    URL='https://api.ultradata.neustar/v1'
   
    auth_response = requests.post(URL+'/authorization/token',
                                 data = {
                                     'grant_type': 'password',
                                     'username': ULTRADATA_USERNAME,
                                     'password': ULTRADATA_PASSWORD
                                 })
    auth = auth_response.json()
    return auth['access_token']


if __name__ == '__main__':
    print(ultradata_login())
