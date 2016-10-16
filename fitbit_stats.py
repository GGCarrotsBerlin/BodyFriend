import fitbit.fitbit_api as fitbit
Nerd=u"\U0001F913'
"""

For the activities/log/calories resource, each data point also includes the level field that reflects calculated activity level for that time period 
( 0 - sedentary; 1 - lightly active; 2 - fairly active; 3 - very active.)
"""

def getOptionText(input_score):
	input_score=str(input_score)
	activitySummary={ "0": 'sedentary', '1' :'lightly active',  '2':'fairly active', '3': 'very active', '-1':"not so active"}
	return activitySummary[input_score]
	
#try:
activitySummary=fitbit.getActivitySummary()
sleepLastNight=fitbit.getSleepLastNight()
#except Error as e:
#	print "something went wrong calling the fitbit api"

fitbit_summary_text='Yesterday you {only} did {steps} steps'.format(steps=activitySummary['steps'],
																							 only='only' if activitySummary["activeScore"]<0 else '',
																							sleep=sleepLastNight)
fitbit_activity_summary='In general, you were {option}. Some stats for you: total distance:<b>{td}</b>, lightly active minutes:<b>{am}</b>, sedentary minutes:<b>{sm}</b>. '.format(
	option=getOptionText(activitySummary['activeScore']),
	td=activitySummary["distances"][0]["distance"],
	am=activitySummary["lightlyActiveMinutes"],
	sm=activitySummary["sedentaryMinutes"]
	)
if activitySummary['activeScore']<=1:
    fitbit_activity_summary2="\n It looks like you were hacking too much ..." + (Nerd *3) 

heart_ratio=fitbit.getHeartRatio()
fitbit_heart_ratio_summary=''
if not heart_ratio is None and not len(heart_ratio)==0:
	for hr in fitbit_heart_ratio_summary:
		try:
			fitbit_heart_ratio_summary+=heart_ratio['name'] + ' ' + heart_ratio['minutes'] + ' minutes,'
		except KeyError as ke:
			continue
	if  not fitbit_heart_ratio_summary=='':
		fitbit_heart_ratio_summary='Here is your heart rate stats: ' + fitbit_heart_ratio_summary
	
print fitbit_heart_ratio_summary
""" Tags in JSON we can use

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

#print fitbit_summary_text
#print fitbit_activity_summary