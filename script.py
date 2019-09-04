import requests  
import datetime
import random
import pickle
import sys

from bothandler import *
from msgstrings import *

# creator chat ID :)
my_chat = 545584095

# list of commands that can't work if the grouplist is empty
commands_list = ['/generate', '/swap', '/move', '/show']
for item in range(len(commands_list)):
    commands_list.append(commands_list[item] + '@exam_queue_bot')
    
def main():    
    new_offset = None

    while True:
        bot.get_updates(new_offset)

        # check for errors and damaged data
        last_update = bot.get_last_update()
        if not(last_update['ok']):
            continue

        try:
            last_update_id = last_update['update_id']
            last_chat_id = last_update['message']['chat']['id']
            last_chat_text = last_update['message']['text']
            last_chat_text = last_chat_text.split('\n')
        except KeyError:
            new_offset = last_update_id + 1
            continue

        # check for attempts to work with an empty list
        if not last_chat_id in bot.grouplists or not bot.grouplists[last_chat_id]:
            if extract_first_word(last_chat_text) in commands_list:
                bot.send_message(empty_list, last_chat_id)
                new_offset = last_update_id + 1
                continue
            
        bot.process_command(last_chat_text, last_chat_id)
            
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    # a token for the bot is passed as an argument.
    bot = BotHandler(sys.argv[1])
    try:
        main()
    except Exception as e:
        bot.send_message(str(type(e)) + str(e), my_chat, markdown = False)
        bot.save()
        exit()