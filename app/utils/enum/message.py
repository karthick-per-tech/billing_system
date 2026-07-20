from enum import Enum

class MessageResponse(str,Enum):
    SUCCESS = "success",
    ERROR = "error",
    NOTFOUND = "Notfound"