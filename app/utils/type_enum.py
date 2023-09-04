# --*-- coding: utf-8 --*--


from enum import Enum, unique

@unique
class ChatCommandType(Enum):
   ChatRoom = 0
   P2P = 1
   CreateRoom = 2
