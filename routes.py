from flask import Flask, render_template, request, Response

from langchain.llms import OpenAI

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator

from typing import List

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

    resp = chatgpt(messages)

    return resp.content

class SustPlantInfo(BaseModel):
  common_name: str = Field(description="The common name to a sustainable plant.")
  sci_name: str = Field(description="The plant's scientific name.")
  desc: str = Field(description="A 2-3 sentence description of the plant and why it is good for a garden.")

class SustPlants(BaseModel):
  plants: List[SustPlantInfo]

def query_sustplants(num):
    plant_query = "Give me" + num + "sustainable plants to plant in California in April."
    parser = PydanticOutputParser(pydantic_object=SustPlants)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    _input = prompt.format_prompt(query=plant_query)

    model = ChatOpenAI(model_name='gpt-3.5-turbo')
    resp = model([HumanMessage(content=_input.text)])

    return resp.content

@app.route('/completion', methods=['GET', 'POST'])
def completion_api():
    if request.method == "POST":
        data = request.form
        input_text = data['input_text']
        return Response(query(input_text), mimetype='text/plain')
    else:
        return Response(None, mimetype='text/plain')
    
@app.route('/sustplants', methods=['POST'])
def sust_plants():
    data = request.form
    num = data['num']
    return Response(query_sustplants(num), mimetype='text/plain')
    
if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(host='0.0.0.0')
