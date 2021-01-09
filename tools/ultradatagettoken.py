#!/usr/bin/python3
import requests

def ultradata_login():

    #todo: use ~/.ultradata/credentials
    #  consider .netrc format, which 'requests' understands - but might be annoying
    #  https://docs.python.org/3/library/netrc.html
    #with open('.replace('\n', '')', 'r') as file:
    #    data = file.readlines()
    
    ULTRA_USERNAME='ultradata-miranda-full'
    ULTRA_PASSWORD='ThePasswordIs1Password'
    URL='https://api.miranda.neustar/v1'
   
    auth_response = requests.post(URL+'/authorization/token',
                                 data = {
                                     'grant_type': 'password',
                                     'username': ULTRA_USERNAME,
                                     'password': ULTRA_PASSWORD
                                 })
    #throw something if there is any problem with the authentication
    auth = auth_response.json()
    return auth['access_token']

if __name__ == '__main__':
    print(ultradata_login())
