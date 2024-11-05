from flask import Flask, request, Response
import pandas as pd
import logging 
import json
from GPT_Chart_Gen import PromptResponse
from LLama_Chat_Ability import PromptChat

def setup_logger(log_file='app.log'):
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()])
    return logging.getLogger(__name__)
logger = setup_logger()

app = Flask(__name__)

@app.route('/generate-charts', methods=['POST'] )

def FileHandler():
    ContentType = request.files['Dataset'].content_type
    if "csv" in ContentType:
        request.files['Dataset'].save("fdata.csv")
        return run_csv("fdata.csv")
    elif "excel" in ContentType:
        request.files['Dataset'].save("fdata.xlsx")
        return run_excel("fdata.xlsx")
    else: 
        return Response(f'PLEASE UPLOAD A VALID FILETYPE: uploaded file type is {ContentType} \n Accepted file types are Excel or CSV', mimetype='text/json')

def run_csv(FileName):
    Prompt = request.form.get('Prompt')
    df = pd.read_csv(FileName,nrows=100)
    df.to_csv("downloaded_Dataset.csv",index=False)
    if not Prompt:
        try:
            output = PromptResponse("Please create a chart of your chosing using the following data")
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='text/plain')
    else:
        try:
            output = PromptResponse(Prompt)
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='text/plain')

def run_excel(FileName):
    Prompt = request.form.get('Prompt')
    df = pd.read_excel(FileName,nrows=100)
    df.to_csv("downloaded_Dataset.csv",index=False)   
    if not Prompt:
        try:
            output = PromptResponse("Please create a chart of your chosing using the following data")
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='text/plain')
    else:
        try:
            output = PromptResponse(Prompt)
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='text/plain')

@app.route('/llama/chat', methods=['POST'] )

def MsgHandler():
    UserInput = request.form.get('msg')
    if UserInput:
        return PromptChat(UserInput)
    else: 
        return Response(f'What can I help you with?', mimetype='text/plain')

def llama_chat(UserInput): 
    if not UserInput:
        try:
            Chatting = PromptChat("what can you do?")
        except Exception as e:
            Chatting = str(e)
        return Response(Chatting, mimetype='text/plain')
    else:
        try:
            Chatting = PromptChat(UserInput)
        except Exception as e:
            Chatting = str(e)
        return Response(Chatting, mimetype='text/plain')

if __name__ == '__main__':
    app.run()