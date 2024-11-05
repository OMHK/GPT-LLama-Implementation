from flask import Flask, request, render_template,Response
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

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@app.errorhandler(400)
def internal_error(error):
    return render_template('400.html'), 400

@app.errorhandler(401)
def internal_error(error):
    return render_template('401.html'), 401

@app.errorhandler(403)
def internal_error(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(405)
def not_found_error(error):
    return render_template('405.html'), 405

@app.errorhandler(406)
def not_found_error(error):
    return render_template('406.html'), 406

@app.route('/documentai/generate-charts', methods=['POST'] )

def FileHandler():
    ContentType = request.files['Dataset'].content_type
    if "csv" in ContentType:
        return run_csv(request.files['Dataset'])
    elif "excel" in ContentType:
        return run_excel(request.files['Dataset'])
    else: 
        return Response(f'PLEASE UPLOAD A VALID FILETYPE: uploaded file type is {ContentType} \n Accepted file types are Excel or CSV', mimetype='text/json')

def run_csv(FileName):
    Prompt = request.form.get('Prompt')
    df = pd.read_csv(FileName)
    df.to_csv("downloaded_Dataset.csv",index=False)
    if not Prompt:
        try:
            output = PromptResponse("Please create a chart of your chosing using the following data")
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='application/json')
    else:
        try:
            output = PromptResponse(Prompt)
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='application/json')

def run_excel(FileName):
    Prompt = request.form.get('Prompt')
    df = pd.read_excel(FileName)
    df.to_csv("downloaded_Dataset.csv",index=False)
    if not Prompt:
        try:
            output = PromptResponse("Please create a chart of your chosing using the following data")
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='application/json')
    else:
        try:
            output = PromptResponse(Prompt)
        except Exception as e:
            output = str(e)
        return Response(output, mimetype='application/json')

@app.route('/documentai/llama/chat', methods=['POST'] )

def MsgHandler():
    UserInput = request.form.get('msg')
    if UserInput:
        return PromptChat(UserInput)
    else: 
        return Response(f'What can I help you with?', mimetype='application/json')

def llama_chat(UserInput): 
    if not UserInput:
        try:
            Chatting = PromptChat("what can you do?")
        except Exception as e:
            Chatting = str(e)
        return Response(Chatting, mimetype='application/json')
    else:
        try:
            Chatting = PromptChat(UserInput)
        except Exception as e:
            Chatting = str(e)
        return Response(Chatting, mimetype='application/json')

if __name__ == '__main__':
    app.run()