import requests  
import datetime
import random
import pickle
import sys

from bothandler import BotHandler
from msgstrings import *

my_chat = 545584095
now = datetime.datetime.now()

commands_list = ['/generate', '/swap', '/move', '/exception', '/show']
length = len(commands_list)
for item in range(length):
    commands_list.append(commands_list[item] + '@exam_queue_bot')

def command_is(command, last_chat_text):
    word_to_test = last_chat_text[0].split()[0].strip()
    print('A', word_to_test)
    return word_to_test == command or word_to_test == command + '@exam_queue_bot'    

def main():    
    new_offset = None

    while True:
        if now.minute % 10 == 0:
            greet_bot.save()
            
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if not(last_update['ok']):
            continue

        try:
            last_update_id = last_update['update_id']
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
        except KeyError:
            new_offset = last_update_id + 1
            continue

        last_chat_text = last_chat_text.split('\n')
        print(last_chat_text)
        
        if not last_chat_id in greet_bot.grouplists or not greet_bot.grouplists[last_chat_id]:
            if last_chat_text[0].split()[0].strip() in commands_list:
                greet_bot.send_message(empty_list, last_chat_id)
                new_offset = last_update_id + 1
                continue
            
        if command_is('/setlist', last_chat_text):
            if len(last_chat_text) < 2:
                greet_bot.send_message(list_creation_error, last_chat_id)
            else:
                greet_bot.send_message('Список сохранён.', last_chat_id)
                greet_bot.set_list(last_chat_text[1:], last_chat_id)
            
        if command_is('/generate', last_chat_text):
            greet_bot.send_message(greet_bot.generate(last_chat_id), 
                                   last_chat_id)
            
        if command_is('/swap', last_chat_text):
            greet_bot.send_message(greet_bot.swap(last_chat_text[0].split()[1:], 
                                                  last_chat_id), last_chat_id)
            
        if command_is('/move', last_chat_text):
            print(last_chat_text)
            greet_bot.send_message(greet_bot.move(last_chat_text[0].split()[1:], 
                                                  last_chat_id), last_chat_id)
            
        if command_is('/exception', last_chat_text):
            raise Exception('Test falling thrown by ' 
                            + last_update['message']['from']['username'])

        if command_is('/show', last_chat_text):
            greet_bot.send_message(show_success + greet_bot.list_to_txt(last_chat_id), 
                                   last_chat_id)

        if command_is('/info', last_chat_text):
            greet_bot.send_message(information, last_chat_id)
            
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    print(sys.argv[0])
    # a token for the bot is passed as an argument.
    greet_bot = BotHandler(sys.argv[1])
    try:
        main()
    except Exception as e:
        greet_bot.send_message(str(type(e)) + str(e), my_chat, markdown = False)
        greet_bot.save()
        greet_bot.send_message('Saved!', my_chat)
        exit()