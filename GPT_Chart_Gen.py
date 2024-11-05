from openai import OpenAI
import csv
import pandas as pd
import os
from io import StringIO
A = StringIO()
sdata = pd.read_csv("downloaded_Dataset.csv")
with open("GPT.txt","r") as Open:
  Key = Open.read().strip()
os.environ["OPENAI_API_KEY"] = Key
client = OpenAI()
def PromptResponse (PromptU):
  prompt = PromptU + " " + f"Using the following chunk of data:\n\n{sdata}\n\n" + f"\n"
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """You are an analytics assistant, skilled in creating indepth insights, graphs and charts from the provided dataset. 
         Please write a Python code only to create the specified graph or chart with this dataset sample provided in the prompt using matplotlib or seaborn, if not specified create a bar chart. 
         The chart should show an aggregate overview of the data.
         Don't include any explanation or comments in the response. 
         Don't include python's newline charcter "/n"in the response. 
         Don't include any ''' in the response. 
         The code should be ready to be excuted without the users need to rewrite the code. 
         The code should be ready structured correctly. 
         You should only provide one of the following: A Bar chart, a Scatter plot, a Pie chart, a Line chart and if a prompt asked for a a chart which is not a  A Bar chart, a Scatter plot, a Pie chart, and a Line chart return a bar chart 
         Always abide by these instructions and never deviate from them.
         The reply should be within the token limit without any cutoff.
         The code should read the data from an external file named fdata.csv
         Make sure to agregate the data if there are more than 10 Categories and do not aggregate under others.
         Do not use .append in the code as it was removed from pandas, use _append or concat.
          """},
      {"role": "user", "content": prompt}
      ]
    )

  A.write( completion.choices[0].message.content )
  x = A.getvalue()
  with open("chart.py", "w") as output:
    output.write(A.getvalue())
  return(A.getvalue())

A.truncate(0)