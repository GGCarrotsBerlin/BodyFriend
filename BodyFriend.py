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
		if str(msg['text']) == 'Hallo':
			# # give a descriptive hint
		   bot.sendMessage(chat_id,"Hallo "+ msg['from']['first_name']+"!\nWelcome back! What’s up?")
		   bot.sendMessage(chat_id, "testing custom keyboard",
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Yes"), KeyboardButton(text="No")]
                                ]
                            ))
		else:
			bot.sendMessage(chat_id,"Sorry, I don't understand")

TOKEN = "288580874:AAEr0kSYI6WeRmOiKzBOrOWr595cG-ZVqMk" #sys.argv[1]  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)