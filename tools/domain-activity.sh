#!/bin/sh

if [ -z "$1" -o "$1" = "-help" ] ; then
    echo "Usage:"
    echo "  $0 {starttime} {endtime} < {name-list}"
    echo "e.g."
    echo "  echo neustar.biz | $0 1601292900 1601071800"
    echo
    echo "times are any datetime string that can be interpreted by 'date'"
    echo
    echo "This script stores credentials in ~/.ultradata and will prompt to"
    echo "create them if they do not exist"
    echo
    exit 1
fi

`dirname $0`/get-token.sh
if [ "$?" -ne 0 ] ; then
    exit 2
fi

date +"%s" -d "2020-01-01" 2> /dev/null
if [ "$?" -ne 0 ] ; then
    which gdate > /dev/null
    if [ "$?" -ne 0 ] ; then
	echo "Need to convert human dates to timestamps - install gdate?"
	exit 3
    else
	DATE=gdate
    fi
else
    DATE=date
fi


ULTRA_TOKEN=`cat ~/.ultradata/token`
STARTTIME=`$DATE +"%s" -d $1`
if [ "$?" -ne 0 ] ; then
    exit 4
fi
ENDTIME=`$DATE +"%s" -d $2`
if [ "$?" -ne 0 ] ; then
    exit 4
fi

echo "domain,stubCount,hostIpCount,subdomainCount,nameserverCount"
while read DOMAIN ; do
    export LOCATION="https://api.ultradata.neustar/v1/domain/activity?domain=$DOMAIN&starttime=$STARTTIME&endtime=$ENDTIME"
    while [ "$LOCATION" -a "$LOCATION" != "null" ] ; do
	export QUERY_RESULT=`curl -s -L -X GET $LOCATION -H "Authorization: Bearer $ULTRA_TOKEN"`

	#a token error will happen when the token expires - e.g. after 60min
	ERRORCODE=`echo $QUERY_RESULT | jq .errorCode`
	if [ "$ERRORCODE" -a "$ERRORCODE" = "401" ] ; then
	    rm ~/.ultradata/token
	    `dirname $0`/get-token.sh
	    ULTRA_TOKEN=`cat ~/.ultradata/token`
	    #do not reset LOCATION in this case
	    
	else
	
	    #in the case of a http 202 response, the Poll document contains
	    #  {"location": -url-, "poll-interval-s": -num-}
	    export LOCATION=`echo $QUERY_RESULT | jq -r '.location'`
	    if [ "$LOCATION" -a "$LOCATION" != "null" ] ; then
		sleep `echo $QUERY_RESULT | jq '."poll-interval-s"'`
	    fi
	fi

	#anything other than a 401 error or a 202 with a location will fall through
	#  including success and any other error condition

	#e.g. {"errorCode": 60001, "errorDescription": "Query interval is longer than 14 days (1590984000-1588305600=2678400)"}
	#     

    done
    if [ `echo $QUERY_RESULT | jq -r '.stubCount'` = "null" ] ; then
	echo $QUERY_RESULT
    else
	echo $QUERY_RESULT | jq -r '. | "'$DOMAIN', \(.stubCount), \(.hostIpCount), \(.subdomainCount), \(.nameserverCount)"'
    fi
	
done

