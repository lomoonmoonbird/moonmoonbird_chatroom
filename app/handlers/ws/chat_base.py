# --*-- coding: utf-8 --*--


class ChatBase():
    def __init__(self):
        self.connect_users = []
        self.chat_database = "moonmoonbird_chat"
        self.messages_collection = "messages"
        self.online_user = "onlines"
        self.mongo_db = None