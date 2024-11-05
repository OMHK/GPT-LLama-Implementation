from openai import OpenAI
import csv
import os
from io import StringIO
A = StringIO()
def chunking(file_path, chunk_size=105):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        chunk = []
        for row in reader:
            chunk.append(row)
            if len(chunk) == chunk_size:
                yield chunk 
                chunk = []

os.environ["OPENAI_API_KEY"] = "Token"
client = OpenAI()
def PromptResponse (PromptU):
  for chunk in chunking("./downloaded_Dataset.csv"):
    chunk_as_string = "\n".join([",".join(row) for row in chunk])
    prompt = PromptU + " " + f"Using the following chunk of data:\n\n{chunk_as_string}\n\n" + f"\n"
    completion = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": """You are an analytics assistant, skilled in creating indepth insights, graphs and charts from the provided dataset. 
         Please write a JSON code only to create the specified graph or chart with this full dataset provided in the prompt, if not specified create a bar chart. 
         The chart should show an aggregate overview of the data>
         There must not be a need to read data from an external file when creating the chart.
         Don't include any explanation or comments in the response. 
         Don't include python's newline charcter "/n"in the response. 
         Don't include any ''' in the response. 
         The Json code should be ready to be excuted without the users need to rewrite the code. 
         The code should be ready structured correctly. 
         You should only provide one of the following: A Bar chart, a Scatter plot, a Pie chart, a Line chart and if a prompt asked for a a chart which is not a  A Bar chart, a Scatter plot, a Pie chart, and a Line chart return a bar chart 
         The JSON code should follow the following format "type", "data", "labels", "datasets", "label", "data".
         The JSON code should not include backgroundColor
         Never include the Options part.
         Always abide by these instructions and never deviate from them.
         The reply should be within the token limit without any cutoff.
         Limit the chart to only have 10 Categroies 
         please include a comma (,) followed by a space at the end of the each JSON object
          """},
        {"role": "user", "content": prompt}
      ]
    )

    A.write( completion.choices[0].message.content )

  return(A.getvalue())
A.truncate(0)
