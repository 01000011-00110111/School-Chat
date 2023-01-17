"""Filter usernames and make the chat more xss safe"""
from bs4 import BeautifulSoup


def filter_username(message):
    message_profile = message.split("</img>")
    messages = message_profile[1].split("-")
    soup = BeautifulSoup(messages[0], "html.parser")
    tags = soup.font

    if (tags.string == None):
        tags.string = "Anonymous"
    elif (tags.string == "Admin" or tags.string == "admin"
          or tags.string == "[admin]" or tags.string == "[admin]"
          or tags.string == "[ADMIN]" or tags.string == "ADMIN"):
        return
    elif (tags.string == "mod" or tags.string == "Mod"
          or tags.string == "[mod]" or tags.string == "[Mod]"
          or tags.string == "[MOD]" or tags.string == "MOD"):
        return
    elif (tags.string == "Dev EReal"):
        tags.string = "Dev E"
    elif (tags.string == "Dev E"):
        return
    elif (tags.string == "cserverReal"):
        tags.string = "cserver"
    elif (tags.string == "cserver"):
        return
    elif (tags.string == "SYSTEM" or tags.string == "[SYSTEM]"):
        return
    messages[0] = str(soup)
    msg = ""
    for message_e in messages:
        msg = msg + message_e + "-"

    msg = msg.rstrip(msg[-1])
    return msg
