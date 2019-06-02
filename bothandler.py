import requests  
import datetime
import random
import pickle

from msgstrings import *

pickle_file = 'Queue bot.pkl'

class BotHandler:
    grouplists = {}
    
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        with open(pickle_file, 'rb') as f:
            self.grouplists = pickle.load(f)
            f.close()

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        try:
            result_json = resp.json()['result']
        except KeyError:
            result_json = {}
        return result_json

    def send_message(self, text, chat_id, markdown = True):
        params = {'chat_id': chat_id, 'text': text}
        if markdown:
            params['parse_mode'] = 'Markdown'
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def list_to_txt(self, chat_id):
        result_txt = ''
        index = 1
        for item in self.grouplists[chat_id]:
            result_txt += str(index) + '. ' + item + '\n'
            index += 1
        return result_txt
    
    def get_last_update(self):
        get_result = self.get_updates()

        last_update = {}
        if len(get_result) > 0:
            last_update = get_result[-1]
            last_update['ok'] = True
        else:
            last_update['ok'] = False
        return last_update
    
    def set_list(self, text, chat_id):
        self.grouplists[chat_id] = text
        self.save()
        
    def generate(self, chat_id):
        random.shuffle(self.grouplists[chat_id])
        self.save()
        return generate_success + self.list_to_txt(chat_id)
    
    def get_numbers(self, indexes, chat_id):
        answer = list()
        for index in indexes:
            try:
                answer.append(int(index) - 1)
            except ValueError:
                num = 0
                added = False
                for item in self.grouplists[chat_id]:
                    if index.strip() == item.split()[0].strip():
                        answer.append(num)
                        added = True
                        break
                    num += 1
                if not(added):
                    answer.append(-1)
        return answer
          
    def check_indexes(self, indexes, chat_id):
        for index in indexes:
            if index < 0 or index >= len(self.grouplists[chat_id]):
                return False
        return True
        
    def swap(self, indexes, chat_id):
        if len(indexes) != 2:
            return swap_error
        
        indexes = self.get_numbers(indexes, chat_id)
        if not(self.check_indexes(indexes, chat_id)):
            return swap_error
        
        cur_list = self.grouplists[chat_id]
        cur_list[indexes[0]], cur_list[indexes[1]] = cur_list[indexes[1]], cur_list[indexes[0]]
        self.save()
        return move_success + self.list_to_txt(chat_id)
    
    def move(self, indexes, chat_id):
        if len(indexes) != 2:
            return move_error
        
        indexes = self.get_numbers(indexes, chat_id)
        if not(self.check_indexes(indexes, chat_id)):
            return move_error
        
        cur_list = self.grouplists[chat_id]
        if indexes[0] < indexes[1]:
            indexes[1] += 1
        cur_list.insert(indexes[1], cur_list[indexes[0]])
        if indexes[0] >= indexes[1]:
            indexes[0] += 1
            
        cur_list.pop(indexes[0])
        self.save()
        return move_success + self.list_to_txt(chat_id)
    
    def save(self):
        with open(pickle_file, 'wb') as f:
            pickle.dump(self.grouplists, f)
            f.close()