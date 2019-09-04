import requests  
import datetime
import random
import pickle

from msgstrings import *

def first_match(iterable, predicate):
    try:
        return next(idx for idx,n in enumerate(iterable) if predicate(n))
    except StopIteration:
        return -1
    
def extract_first_word(message):
    """ 
    @param message: list of strings where each item is a paragraph in the message
    @rtype: string
    """
    return message[0].split()[0].strip()

def extract_args(message):
    """ 
    @param message: list of strings where each item is a paragraph in the message
    @rtype: list of string args passed with the command
    """
    return message[0].split()[1:]

def command_is(command, text):
    """ 
    @param command: a string containing the command to compare
    @param text: a list of strings
    @return: bool depending on whether the text is a given command
    """
    word_to_test = extract_first_word(text)
    return word_to_test == command or word_to_test == command + '@exam_queue_bot' 

class BotHandler:
    grouplists = {}
    
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.load()

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        try:
            result_json = resp.json()['result']
        except KeyError:
            result_json = {}
        return result_json
    
    def get_last_update(self):
        get_result = self.get_updates()

        last_update = {}
        if len(get_result) > 0:
            last_update = get_result[-1]
            last_update['ok'] = True
        else:
            last_update['ok'] = False
        return last_update

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
    
    def set_list(self, text, chat_id):
        """
        Saves the given list
        @type text: list of str
        @type chat_id: int
        """
        self.grouplists[chat_id] = text
        self.save()
        
    def generate(self, chat_id):
        """
        Generates a new queue and forms the answer
        @type chat_id: int
        @return: string containing the answer of the bot
        """
        
        random.shuffle(self.grouplists[chat_id])
        self.save()
        return generate_success + self.list_to_txt(chat_id)
    
    def get_numbers(self, arguments, chat_id):
        """
        If there are people recorded with surnames, 
        converts them into indexes in the list
        
        @type arguments: list of str
        @type chat_id: int
        
        @return: list of int
        """
        answer = list()
        for arg in arguments:
            if arg.isdigit():
                answer.append(int(arg) - 1)
            else:
                answer.append(first_match(self.grouplists[chat_id], 
                                          lambda x: x.split()[0] == arg))
        return answer
          
    def check_indexes(self, indexes, chat_id):
        for index in indexes:
            if index < 0 or index >= len(self.grouplists[chat_id]):
                return False
        return True
        
    def swap(self, indexes, chat_id):
        """
        Swaps persons under two given indexes
        
        @type indexes: list of int
        @type chat_id: int
        
        @return: string containing the answer of the bot
        """
        
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
        """
        Moves a person under the first index to the second index
        
        @type indexes: list of int
        @type chat_id: int
        
        @return: string containing the answer of the bot
        """
        
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
    
    def process_command(self, message, chat_id):
        """
        A method that handles all available commands
        
        @param message: list of strings where each item is a paragraph in the message
        @chat_id: int, the chat id from which the message came
        
        """
        if command_is('/setlist', message):
            if len(message) < 2:
                self.send_message(list_creation_error, chat_id)
            else:
                self.send_message('Список сохранён.', chat_id)
                self.set_list(message[1:], chat_id)
            
        if command_is('/generate', message):
            self.send_message(self.generate(chat_id), 
                                   chat_id)
            
        if command_is('/swap', message):
            self.send_message(self.swap(extract_args(message), chat_id), 
                              chat_id)
            
        if command_is('/move', message):
            self.send_message(self.move(extract_args(message), chat_id), 
                              chat_id)
            
        if command_is('/exception', message):
            raise Exception('Test falling thrown by ' 
                            + last_update['message']['from']['username'])
    
        if command_is('/show', message):
            self.send_message(show_success + self.list_to_txt(chat_id), 
                                   chat_id)
    
        if command_is('/info', message):
            self.send_message(information, chat_id)
        
    def save(self):
        pass
        # TODO
        
    def load(self):
        pass
        # TODO