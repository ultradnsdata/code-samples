#!/bin/sh


which curl > /dev/null
if [ "$?" -ne 0 ] ; then
    echo "curl is required - please install and retry"
    exit 1
fi
which jq > /dev/null
if [ "$?" -ne 0 ] ; then
    echo "jq is required - please install and retry"
    exit 1
fi



if [ ! -e ~/.ultradata -o ! -e ~/.ultradata/credentials ] ; then 
    
    read -p "username: " ULTRA_USERNAME
    read -p "password: " ULTRA_PASSWORD

    mkdir -p ~/.ultradata
    chmod 700 ~/.ultradata
    echo "ULTRA_USERNAME=$ULTRA_USERNAME" > ~/.ultradata/credentials
    echo "ULTRA_PASSWORD=$ULTRA_PASSWORD" >> ~/.ultradata/credentials
    chmod 600 ~/.ultradata/credentials
else
    . ~/.ultradata/credentials
fi

if [ ! -e ~/.ultradata/token ] ; then
    ULTRA_TOKEN=`curl -s --request POST 'https://api.ultradata.neustar/v1/authorization/token' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'grant_type=password' --data-urlencode "username=$ULTRA_USERNAME" --data-urlencode "password=$ULTRA_PASSWORD" | jq -r .access_token`
    if [ "null" = "$ULTRA_TOKEN" ] ; then
	echo "Authentication failed"
	exit 2
    else
	echo $ULTRA_TOKEN > ~/.ultradata/token
    fi
fi

exit 0
