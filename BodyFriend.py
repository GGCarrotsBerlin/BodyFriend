import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton


#test commit 

def handle(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(content_type, chat_type, chat_id)

	if content_type == 'text':
		#bot.sendMessage(chat_id, msg['from']['first_name'])
		#print(msg['text'])
		input = str(msg['text']).lower()
		if input == 'hallo' or input == 'hi':
			# # give a descriptive hint
		   bot.sendMessage(chat_id,"Hallo "+ msg['from']['first_name']+"!\nWelcome back!")
		   bot.sendMessage(chat_id, "What’s up?",
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Have a question"), KeyboardButton(text="Wanna track symptoms")]
                                ], 
								resize_keyboard=True,
								one_time_keyboard=True
                            ))#,force_reply=True)
		elif input == 'have a question':
			bot.sendMessage(chat_id,"Just tell me!")
		elif 'period' in input:
			#time.sleep(0.9)
			bot.sendMessage(chat_id,"OK. Let’s stay cool for a minute ok? I will check some data.")
			time.sleep(1.5)
			bot.sendMessage(chat_id,"Ok, I got something.")
			time.sleep(1.5)
			bot.sendMessage(chat_id,"Your average cycle is 28 days. Today you are on day 30.")
			bot.sendMessage(chat_id,"\nDelays of <b>2-4 days are very usual and normal</b>.",parse_mode="HTML")
			time.sleep(1.5)
			bot.sendMessage(chat_id,"In Berlin alone, 67% of women your age. \nhave periods delayed by 3 days at least 5 times a year.")
	
		elif input == 'wanna track symptoms':
			bot.sendMessage(chat_id,"test2")
		else:
			bot.sendMessage(chat_id,"Sorry, I can't understand")

TOKEN = "288580874:AAEr0kSYI6WeRmOiKzBOrOWr595cG-ZVqMk" #sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)