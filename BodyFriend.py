#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, re
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('UTF8')
ThumbUp   = u"\U0001F44D" # Thumb up
ThumbDown = u"\U0001F44E" # Thumb Down
Fear= u"\U0001F631"
from fitbit_stats import fitbit_activity_summary, fitbit_summary_text, fitbit_heart_ratio_summary, sleepLastNight
import ipool.ipool_api as ipool
from articles import articles_feed

keywords="medical research women"
medical_article_feed=ipool.getArticleFeed(keywords)


def choice(chat_id,label,ch1,ch2):
	bot.sendMessage(chat_id, label,
								reply_markup=ReplyKeyboardMarkup(
									keyboard=[
										[KeyboardButton(text=ch1), KeyboardButton(text=ch2)]
									], 
									resize_keyboard=True,
									one_time_keyboard=True
								))
								
def url(chat_id,intro,label,link):
	bot.sendMessage(chat_id, intro,
								reply_markup=InlineKeyboardMarkup(
									inline_keyboard=[[InlineKeyboardButton(text = label,url = link)]]
									))


def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)

	if content_type == 'text':
		#bot.sendMessage(chat_id, msg['from']['first_name'])
		#print(msg['text'])
		input = str(msg['text']).lower()
		if input == 'hallo' or input == 'hi':
			# # give a descriptive hint
		   bot.sendMessage(chat_id,'Hallo '+ msg['from']['first_name']+'!\nWelcome back!')
		   choice(chat_id,'What\'s up?','Have a question','Wanna track symptoms')
		elif re.search('question', input):
			bot.sendMessage(chat_id,'Just tell me!')
		elif 'period' in input:
			#time.sleep(0.9)
			bot.sendMessage(chat_id,'OK. Let’s stay cool for a minute ok? I will check some data.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Ok, I got something.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Your average cycle is 28 days. Today you are on day 30. \nDelays of <b>2-4 days are very usual and normal</b>.',parse_mode='HTML')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'In Berlin alone, 67% of women your age. \nhave periods delayed by 3 days at least 5 times a year.')
			time.sleep(2)
			bot.sendMessage(chat_id, articles_feed[0])
			choice(chat_id,'What now?','Cool, that’s enough.','Anything else?')
		elif input == 'anything else?':
			time.sleep(1.5)
			bot.sendMessage(chat_id,'OK, let me check more data.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'From your temperature and fluids, looks like you ovulated on 3rd Sept. \nThat’s 2 later than your previous cycles.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Your fitbit says you only slept '+ str(sleepLastNight) +' hours for the last night.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'It also says that you have not done any exercise for 10 days.')
			choice(chat_id,'Is it right?','Yes, it\'s right','No, it\'s not right')
		elif input == 'yes, it\'s right':
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Lack of sleep and exercise affect your period. \nYou need to rest more girl!')
			bot.sendMessage(chat_id,articles_feed[1])
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Your resting heartbeat has been higher than usual.')
			time.sleep(1.5)
			choice(chat_id,'Do you feel more stressed than normal?','Yes, a little','No, I\'m not stressed')
		elif input == 'yes, a little':
			bot.sendMessage(chat_id,'Ok, let’s make a plan. \nWe need to bring your stress level down.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'How about a film tonight and sleeping early?')
			choice(chat_id,'New season of Narcos is out on Netflix.','Tell me more','Don\'t want to stay at home')
		elif input == 'no, i\'m not stressed':
			bot.sendMessage(chat_id,'********************')
		elif input == 'no, it\'s not right':
			bot.sendMessage(chat_id,'********************')		
		elif input == 'tell me more':
			#bot.sendMessage(chat_id,'prova**********')		
			url(chat_id,'Help yourself :)','www.netflix.com/Narcos','https://www.netflix.com/title/80025172')
		elif input == 'don\'t want to stay at home':
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Ok, then exercise would be a good idea. \nFresh air and being outdoors.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'You love running.')
			choice(chat_id,'Here are some 5K routes around you from Mapmyrun.','Cool, that’s enough.','Anything else I should do?')
		elif input == 'anything else i should do?':
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Am happy you asked!\nYes, you need to sleep more.')
			time.sleep(1.5)
			choice(chat_id,'Have you tried these teas? \nThey will help you relax and can help with period abnormalities.','That’s cool','I don’t like tea')
		elif input == 'that\'s cool':
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Cool, so plan is: \nRun, drink tea and sleep loads.')
			time.sleep(1.5)
			choice(chat_id,'We wait one day and see what happens OK?','Sounds like a plan','I am still worried')
		elif input == 'sounds like a plan':
			choice(chat_id,'Great. I will remind you to exercise and sleep early OK?',ThumbUp,ThumbDown)
		elif input == 'i am still worried':
			bot.sendMessage(chat_id,'********************')
		elif input == ThumbUp:
			bot.sendMessage(chat_id,'********************')
		elif input == ThumbDown:
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Ok, I won’t disturb you. \nGive your body some rest and exercise.')
			time.sleep(1.5)
			bot.sendMessage(chat_id,'Let’s see what happens. I am here if you need to talk.')
		elif input == 'i don\'t like tea':
			bot.sendMessage(chat_id,'********************')
		elif input == 'wanna track symptoms':
			choice(chat_id,fitbit_summary_text + " " +Fear, "I want more activity data", "thats\'s enough" )
		elif "activity data" in input:
			choice(chat_id,fitbit_activity_summary, "check heart ratio", "thats\'s enough")
		elif "heart ratio" in input:
			if len(fitbit_heart_ratio_summary)==0:
				bot.sendMessage(chat_id, "Hmmm... There is no heart rate data")
			else:
				bot.sendMessage(chat_id,fitbit_heart_ratio_summary)
			
			#choice(chat_id,'Let’s see what happens. I am here if you need to talk.')
		elif re.search("article[.]|news", input):
			if len(medical_article_feed)>0:				
				choice(chat_id, medical_article_feed.pop(), 'More news...', 'Have a question')
			else:
				bot.sendMessage(chat_id, 'Nothing new in the medical world...')
		elif input == 'cool, that\'s enough.':
			bot.sendMessage(chat_id,'I\'m glad it helped!')
		elif re.search('search', input):
			inp_str= input.split(' ')
			print inp_str 
			keywords= (' '.join([inp for inp in inp_str if (len(inp)>3 and inp not in ['search'])]))
			medical_article_feed=ipool.getArticleFeed(keywords)
			if len(medical_article_feed)>0:				
				choice(chat_id, medical_article_feed.pop(), 'More news...', 'Have a question')
			else:
				bot.sendMessage(chat_id, 'No article found... try different search criteria')
			
		else:
			bot.sendMessage(chat_id,'Sorry, I can\'t understand')

TOKEN = '288580874:AAEr0kSYI6WeRmOiKzBOrOWr595cG-ZVqMk' #sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)