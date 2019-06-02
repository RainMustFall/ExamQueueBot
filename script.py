import requests  
import datetime
import random
import pickle

from bothandler import BotHandler
from msgstrings import *

greet_bot = BotHandler('753973018:AAHWhEwQ5L65TecmvUqkTOzSzxeBFQg2JEo')  
my_chat = 545584095
now = datetime.datetime.now()

commands_list = ['/generate', '/swap', '/move', '/exception', '/show']
length = len(commands_list)
for item in range(length):
    commands_list.append(commands_list[item] + '@exam_queue_bot')

def main():  
    new_offset = None

    while True:
        if now.minute % 10 == 0:
            greet_bot.save()
            
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()
        if not(last_update['ok']):
            continue

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
            
        last_chat_text = last_chat_text.split('\n')
        print(last_chat_text, last_chat_id)
        
        if not last_chat_id in greet_bot.grouplists or not greet_bot.grouplists[last_chat_id]:
            if last_chat_text[0].strip() in commands_list:
                greet_bot.send_message(empty_list, last_chat_id)
                new_offset = last_update_id + 1
                continue
            
        if last_chat_text[0].strip() == '/setlist' or last_chat_text[0].strip() == '/setlist@exam_queue_bot':
            if len(last_chat_text) < 2:
                greet_bot.send_message(list_creation_error, last_chat_id)
            else:
                greet_bot.send_message('Список сохранён.', last_chat_id)
                greet_bot.set_list(last_chat_text[1:], last_chat_id)
            
        if last_chat_text[0].strip() == '/generate' or last_chat_text[0].strip() == '/generate@exam_queue_bot':
            greet_bot.send_message(greet_bot.generate(last_chat_id), last_chat_id)
            
        if last_chat_text[0].split()[0] == '/swap' or last_chat_text[0].split()[0] == '/swap@exam_queue_bot':
            greet_bot.send_message(greet_bot.swap(last_chat_text[0].split()[1:], last_chat_id), last_chat_id)
            
        if last_chat_text[0].split()[0] == '/move' or last_chat_text[0].split()[0] == '/move@exam_queue_bot':
            greet_bot.send_message(greet_bot.move(last_chat_text[0].split()[1:], last_chat_id), last_chat_id)
            
        if last_chat_text[0].split()[0] == '/exception' or last_chat_text[0].split()[0] == '/exception@exam_queue_bot':
            raise Exception('Test')

        if last_chat_text[0].split()[0] == '/show' or last_chat_text[0].split()[0] == '/show@exam_queue_bot':
            greet_bot.send_message(show_success + greet_bot.list_to_txt(last_chat_id), last_chat_id)
            
        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except Exception as e:
        greet_bot.send_message(str(type(e)) + str(e), my_chat)
        greet_bot.save()
        greet_bot.send_message('Saved!', my_chat)
        exit()