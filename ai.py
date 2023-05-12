import openai
import os
from colorama import Fore, Style

openai.api_key = os.environ['OPENAI_API_KEY']


def create_responce(message):
    output = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=[{
                                              "role": "user",
                                              "content": message
                                          }])

    print(output)
    responce = "[AI]: <font color='#c40a0a'>" + output['choices'][0]['message']['content'] + "</font>"

    print(Fore.RED + responce + Style.RESET_ALL)
    return responce
