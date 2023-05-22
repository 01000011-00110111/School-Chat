import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']


def create_responce(message, username):
    output = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=[{
                                              "role": "user",
                                              "content": message
                                          }])
    

    print(output["usage"])
    if username == "":
        username = "a user"
    elif username == "csevenReal":
        username = "cseven"
    responce = "<p id='airesponce'>" + username + " asked: " + '"' + message + '"' + "<br>" + "[AI]: " + output['choices'][
        0]['message']['content'] + "</p>"
    return responce
