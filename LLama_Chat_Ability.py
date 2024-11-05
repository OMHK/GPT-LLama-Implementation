import replicate
import os
import json

with open("ReplicateLlama.txt","r") as Open:
  Key = Open.read().strip()
os.environ["REPLICATE_API_TOKEN"] = Key
api = replicate.Client(api_token=os.environ["REPLICATE_API_TOKEN"])

 
History_File = 'Llama_message_history.json'

def save_cht_history(history, filename):
    with open(filename, 'w') as f:
        json.dump(history, f, indent=4)

def load_cht_history(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

cht_history = load_cht_history(History_File)

def log_cht_call(request_data, response_data):
    log_entry = {
        "request": request_data,
        "response": response_data
    }
    cht_history.append(log_entry)
    save_cht_history(cht_history, History_File)

def PromptChat (Prompt):
    output = ""
    load_cht_history(History_File)
    UserPrompt = f"Here is the previous response history {cht_history}, this is the latest prompt: {Prompt}"
    print(cht_history)
    for event in replicate.stream(
    "meta/meta-llama-3-70b-instruct",
    input={
        "top_k": 50,
        "top_p": 0.9,
        "prompt": UserPrompt,
        "max_tokens": 1024,
        "min_tokens": 0,
        "temperature": 0.6,
        "system_prompt": "You are a helpful assistant.",
        "presence_penalty": 0,
        "frequency_penalty": 0},): output += str(event)
    log_cht_call({"endpoint": "Llama", "params": Prompt}, output)
    return(output)