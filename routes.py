from flask import Flask, render_template, request, Response

from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

chatgpt = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0.5)

def query(input_text):
    messages = [
        SystemMessage(content="You are a helpful assistant that tries to answer any questions to the best of your ability. Do not make up answers, simply say 'I don't know' if you are not sure."),
        HumanMessage(content=input_text)
    ]

    response = chatgpt(messages)

    return response.content

@app.route('/completion', methods=['GET', 'POST'])
def completion_api():
    if request.method == "POST":
        data = request.form
        input_text = data['input_text']
        return Response(query(input_text), mimetype='text/plain')
    else:
        return Response(None, mimetype='text/plain')
    
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')
