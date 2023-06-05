#!/bin/bash

the_message=$1

TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
FROM=+18506080295

TO=+15068700919
curl -X POST https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/Messages.json --data-urlencode "Body=$the_message" --data-urlencode "From=${FROM}" --data-urlencode "To=${TO}" -u $TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN
