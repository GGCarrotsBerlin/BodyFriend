import sys
import random
import traceback
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space

"""
$ python3.5 text_input.py <token>
text_input a number:
1. Send the bot anything to start a game.
2. The bot randomly picks an integer between 0-99.
3. You make a text_input.
4. The bot tells you to go higher or lower.
5. Repeat step 3 and 4, until text_input is correct.
"""

class Player(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        #self._answer = random.randint(0,99)


    def open(self, initial_msg, seed):
        self.sender.sendMessage('Welcome on BodyFriend!')
        return True  # prevent on_message() from being called on the initial message

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            self.sender.sendMessage('Say hallo to me please')
            return
        try:
           text_input = msg['text']
        except ValueError:
            self.sender.sendMessage('Say hallo to me please')
            return

        # check the text_input against the answer ...
        if text_input == "Hallo":
            # give a descriptive hint
            self.sender.sendMessage("Hallo")
        else:
            self.sender.sendMessage("Sorry, I don't understand")
            #self.close()

    def on__idle(self, event):
        self.sender.sendMessage('Bye!')
        self.close()


TOKEN = "288580874:AAEr0kSYI6WeRmOiKzBOrOWr595cG-ZVqMk"

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Player, timeout=10),
])
bot.message_loop(run_forever='Listening ...')