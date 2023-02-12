"""Filter usernames and make the chat more xss safe"""
import os
from typing import Union
from bs4 import BeautifulSoup
from flask_socketio import emit
from chat import force_message
#from chat import online


def filter_username(message: str) -> Union[str, bool]:
    """See if an admin as sending the message, otherwise use normal procedure"""
    locked = os.path.exists("backend/chat.lock")
    print(message)
    if message.startswith("<font color='#08bd71'>[SONG]:"
                          ) or message.startswith("[Joke of the day]:"):
        if locked is True:
            return True
        return message

    message_profile = message.split("</img>")
    messages = message_profile[1].split("-")
    soup = BeautifulSoup(messages[0], "html.parser")
    tags = soup.font

    # now do the ones that return (so pylint is happy)
    # also put before it changes the usernames, else itll stop me from sending
    if tags.string in ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN',
                       '[URL]', 'mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD',
                       'SYSTEM', '[SYSTEM]', "SONG", "[Song]", "[SONG]",
                       "[song]", " ", "  ", "   ", "Dev E", "cserver"):
        return None

    # decide if username matches list of possible options.
    if tags.string is None:
        tags.string = "Anonymous"
    elif tags.string == "Dev EReal":
        tags.string = "Dev E"
    elif tags.string == "cserverReal":
        tags.string = "cserver"

    # back to processing
    messages[0] = str(soup)
    msg = ""
    for message_e in messages:
        msg = msg + message_e + "-"

    msg = msg.rstrip(msg[-1])

    if tags.string in ("Dev E", "cserver"):
        force_message(msg)
        emit("message_chat", msg, broadcast=True, namespace="/")
        return True

    if locked is True:
        return True
    return msg
