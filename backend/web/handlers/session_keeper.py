import random


class SessionKeeper:
    def __init__(self, logger):
        self.logger = logger
        self.user_to_session = {}

    def add_session(self, user_id):
        symbols = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z',
                   'x', 'c',
                   'v', 'b', 'n', 'm', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H',
                   'J', 'K',
                   'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        key = ''
        for _ in range(16):
            key += random.choice(symbols)
        self.user_to_session[user_id] = key
        return key

    def check_session(self, user_session):
        if user_session in self.user_to_session.values():
            for key in self.user_to_session.keys():
                if self.user_to_session[key] == user_session:
                    return key
        return None

    def delete_session(self, user_session):
        if user_session in self.user_to_session.values():
            for key in self.user_to_session.keys():
                if self.user_to_session[key] == user_session:
                    del self.user_to_session[key]
                    break
