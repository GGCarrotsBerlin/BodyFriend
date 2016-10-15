import base64
import urllib2
import urllib

#These are the secrets etc from Fitbit developer

OAuthTwoClientID = "228396"
ClientOrConsumerSecret = "70605de0b8bb97c110633fa4076eab8f"

#This is the Fitbit URL
TokenURL = "https://api.fitbit.com/oauth2/token"

#I got this from the first verifier part when authorising my application
#AuthorisationCode = "c6b5a8b60d10e9c2c51361b1114db05f5ae11822#_=_"
AuthorisationCode = "c6b5a8b60d10e9c2c51361b1114db05f5ae11822"
#Form the data payload
BodyText = {'code' : AuthorisationCode,
            'redirect_uri' : 'http://eatworklove.de/',
            'client_id' : OAuthTwoClientID,
            'grant_type' : 'authorization_code'}

BodyURLEncoded = urllib.urlencode(BodyText)
print BodyURLEncoded




#Start the request
req = urllib2.Request(TokenURL,BodyURLEncoded)

#Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
req.add_header('Authorization', 'Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
req.add_header('Content-Type', 'application/x-www-form-urlencoded')

#Fire off the request
try:
  response = urllib2.urlopen(req)

  FullResponse = response.read()

  print "Output >>> " + FullResponse
except urllib2.URLError as e:
  print e.code
  print e.read()