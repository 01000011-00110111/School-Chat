import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']


def create_responce(message):
    output = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                          messages=[{
                                              "role": "user",
                                              "content": message
                                          }])

    print(output["usage"])
    responce = "<p id='airesponce'>[AI]: " + output['choices'][
        0]['message']['content'] + "</p>"
    return responce
