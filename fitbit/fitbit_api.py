import base64
import urllib2
import urllib
import sys
import json
import os

#This is the Fitbit URL to use for the API call
FitbitURL ="V"
#FitbitURL = "https://api.fitbit.com/1/user/-/heartbeat.json"
#FitbitURL =  "https://api.fitbit.com/1/user/-/activities/date/2016-10-15.json"
#Use this URL to refresh the access token
TokenURL = "https://api.fitbit.com/oauth2/token"
#dir_path=os.path.dirname(__file__)
#dir_path=os.getcwd()
dir_path=os.path.dirname(os.path.abspath(__file__))
#Get and write the tokens from here
IniFile = dir_path +"/tokens.txt"

#From the developer site
OAuthTwoClientID = "228396"
ClientOrConsumerSecret = "70605de0b8bb97c110633fa4076eab8f"

#Some contants defining API error handling responses
TokenRefreshedOK = "Token refreshed OK"
ErrorInAPI = "Error when making API call that I couldn't handle"

#Get the config from the config file.  This is the access and refresh tokens
def GetConfig():
  print "Reading from the config file"

  #Open the file
  FileObj = open(IniFile,'r')

  #Read first two lines - first is the access token, second is the refresh token
  AccToken = FileObj.readline()
  RefToken = FileObj.readline()

  #Close the file
  FileObj.close()

  #See if the strings have newline characters on the end.  If so, strip them
  if (AccToken.find("\n") > 0):
    AccToken = AccToken[:-1]
  if (RefToken.find("\n") > 0):
    RefToken = RefToken[:-1]

  #Return values
  return AccToken, RefToken

def WriteConfig(AccToken,RefToken):
  print "Writing new token to the config file"
  print "Writing this: " + AccToken + " and " + RefToken

  #Delete the old config file
  os.remove(IniFile)

  #Open and write to the file
  FileObj = open(IniFile,'w')
  FileObj.write(AccToken + "\n")
  FileObj.write(RefToken + "\n")
  FileObj.close()

#Make a HTTP POST to get a new
def GetNewAccessToken(RefToken):
  print "Getting a new access token"

  #Form the data payload
  BodyText = {'grant_type' : 'refresh_token',
              'refresh_token' : RefToken}
  #URL Encode it
  BodyURLEncoded = urllib.urlencode(BodyText)
  print "Using this as the body when getting access token >>" + BodyURLEncoded

  #Start the request
  tokenreq = urllib2.Request(TokenURL,BodyURLEncoded)

  #Add the headers, first we base64 encode the client id and client secret with a : inbetween and create the authorisation header
  tokenreq.add_header('Authorization', 'Basic ' + base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
  tokenreq.add_header('Content-Type', 'application/x-www-form-urlencoded')

  #Fire off the request
  try:
    tokenresponse = urllib2.urlopen(tokenreq)

    #See what we got back.  If it's this part of  the code it was OK
    FullResponse = tokenresponse.read()

    #Need to pick out the access token and write it to the config file.  Use a JSON manipluation module
    ResponseJSON = json.loads(FullResponse)

    #Read the access token as a string
    NewAccessToken = str(ResponseJSON['access_token'])
    NewRefreshToken = str(ResponseJSON['refresh_token'])
    #Write the access token to the ini file
    WriteConfig(NewAccessToken,NewRefreshToken)

    print "New access token output >>> " + FullResponse
  except urllib2.URLError as e:
    #Gettin to this part of the code means we got an error
    print "An error was raised when getting the access token.  Need to stop here"
    print e.code
    print e.read()
    sys.exit()

#This makes an API call.  It also catches errors and tries to deal with them
def MakeAPICall(InURL,AccToken,RefToken):
  #Start the request
  print InURL
  req = urllib2.Request(InURL)

  #Add the access token in the header
  req.add_header('Authorization', 'Bearer ' + AccToken)

  #print "I used this access token " + AccToken
  #Fire off the request
  try:
    #Do the request
    response = urllib2.urlopen(req)
    #Read the response
    FullResponse = response.read()

    #Return values
    return True, FullResponse
  #Catch errors, e.g. A 401 error that signifies the need for a new access token
  except urllib2.URLError as e:
    print "Got this HTTP error: " + str(e.code)
    HTTPErrorMessage = e.read()
    print "This was in the HTTP error message: " + HTTPErrorMessage
    #See what the error was
    if (e.code == 401) and (HTTPErrorMessage.find("expired_token") > 0):
      GetNewAccessToken(RefToken)
      return False, TokenRefreshedOK
    #Return that this didn't work, allowing the calling function to handle it
    return False, ErrorInAPI
  
def retrieveData(FitbitURL, retry_flag=False):
  #Main part of the code
  #Declare these global variables that we'll use for the access and refresh tokens
  AccessToken = ""
  RefreshToken = ""
  
  #Get the config
  AccessToken, RefreshToken = GetConfig()
  #Make the API call
  APICallOK, APIResponse = MakeAPICall(FitbitURL, AccessToken, RefreshToken)
  json_resp={}
  if APICallOK:
    try:
      json_resp=(json.loads(APIResponse))
    except KeyError as k:
      print "something went wrong parsing the data {0}".format(total_sleep)
  else:
    if (APIResponse == TokenRefreshedOK and retry_flag is False):
      print "Refreshed the access token.  Can go again"
      APICallOK,total_sleep=retrieveData(FitbitURL, retry_flag=True)
    else:
      print ErrorInAPI
      
  return APICallOK,json_resp
  
def getSleepLastNight(retry_flag=False):

  FitbitURL='https://api.fitbit.com/1/user/-/sleep/minutesAsleep/date/today/2016-10-15.json'
  #Make the API call
  APICallOK, json_resp = retrieveData(FitbitURL)
  total_sleep=4.3
  if APICallOK:
    try:
      total_sleep=float(json_resp['sleep-minutesAsleep'][0]["value"])/60
    except KeyError as k:
      print "something went wrong parsing the data {0}".format(total_sleep)
   ##print APIResponse
  print json_resp
  return max(total_sleep , 4.3)

def getActivitySummary():

  FitbitURL='https://api.fitbit.com/1/user/-/activities/date/2016-10-15.json'
  #Make the API call
  APICallOK, json_resp = retrieveData(FitbitURL)
  try:
    json_resp=json_resp["summary"]
    #print json_resp
  except KeyError  as er:
    print "No Activity Summary available {er}".format(er=er)
  print json_resp
  return json_resp


def getHeartRatio():
  FitbitURL='https://api.fitbit.com/1/user/-/activities/heart/date/2016-10-15/1d.json'
  APICallOK, json_resp = retrieveData(FitbitURL)
  try:
    #print json_resp
    #print (json_resp['activities-heart'][0]['value']['heartRateZones'])
    json_resp=(json_resp['activities-heart'][0]['value']['heartRateZones'])
    #print json_resp
  except KeyError  as er:
    print 'No heart rate zones {er}'.format(er=er)
  print json_resp
  return json_resp


#keywords="female hygiene late period"
#res=getArticleFeed(keywords)
#nicePrintOut( res)	
									  
			


"""
print "Fitbit API Test Code"

total_sleep  = getSleepLastNight()
print total_sleep
activity_summary=getActivitySummary()
print activity_summary["steps"]

  
 Tags in JSON we can use

distances -> [{u'distance': 0.44, u'activity': u'total'}, {u'distance': 0.44, u'activity': u'tracker'}, {u'distance': 0, u'activity': u'loggedActivities'}, {u'distance': 0, u'activity': u'veryActive'}, {u'distance': 0, u'activity': u'moderatelyActive'}, {u'distance': 0.4, u'activity': u'lightlyActive'}, {u'distance': 0, u'activity': u'sedentaryActive'}]
sedentaryMinutes -> 1216
lightlyActiveMinutes -> 34
caloriesOut -> 1419
caloriesBMR -> 1310
marginalCalories -> 41
fairlyActiveMinutes -> 0
veryActiveMinutes -> 0
activityCalories -> 99
steps -> 590
activeScore -> -1
"""

#print getHeartRatio()
