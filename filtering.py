"""Filter usernames and make the chat more xss safe"""
from bs4 import BeautifulSoup
#from chat import online


def filter_username(message):
    message_profile = message.split("</img>")
    messages = message_profile[1].split("-")
    soup = BeautifulSoup(messages[0], "html.parser")
    tags = soup.font

    # decide if username matches list of possible options.
    if tags.string is None:
        tags.string = "Anonymous"
    elif tags.string == "Dev EReal":
        tags.string = "Dev E"
    elif tags.string == "cserverReal":
        tags.string = "cserver"

    # now do the ones that return (so pylint is happy)
    if tags.string in ('Admin', 'admin', '[admin]', '[ADMIN]', 'ADMIN'):
        return None
    elif tags.string in ('mod', 'Mod', '[mod]', '[Mod]', '[MOD]', 'MOD'):
        return None
    elif tags.string == "Dev E":
        return None
    elif tags.string == "cserver":
        return None
    elif tags.string in ('SYSTEM', '[SYSTEM]'):
        return None

    # back to processing
    messages[0] = str(soup)
    msg = ""
    for message_e in messages:
        msg = msg + message_e + "-"

    msg = msg.rstrip(msg[-1])
    return msg
