# Reference: https://console.groq.com/login
# Store API key in .env file

from dotenv import load_dotenv, find_dotenv
import base64
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import os

#%% Load API Key
load_dotenv(find_dotenv(usecwd=True))
#%% Show API Key
import os
x=os.getenv("GROQ_API_KEY")
print(x)
from langchain_groq import ChatGroq

# When model os bothered with request, change to another (lower complexity ;-( ) model
# "deepseek-r1-distill-qwen-32b" # cannot extract text
# "claude-3-sonnet-20240229"
# "deepseek-r1-distill-qwen-32b"
# "llama-3.2-11b-vision-preview"
# "llama-3.2-90b-vision-preview" # good for text extraction
MODEL_NAME = "llama-3.3-70b-versatile"
MODEL_NAME_VISION = "llama-3.2-11b-vision-preview"
model_vision = None
model = None

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

documents=[f"data/Text {i}.jpg" for i in [1,2,3,4]]
for doc in documents: 
  tdoc=doc+".txt"
  if not os.path.exists(tdoc):
    base64_image = encode_image(doc)
    image_url = f"data:image/jpeg;base64,{base64_image}"
    aufgaben_message = HumanMessage(
        content=[
            # <maef> partout nicht moeglich, dass das Layout beibehalten wird!
            {"type": "text", "text": "Extrahiere aus dem Bild in der Orginalsprache den Text mit allen Fehlern und behalte das Layout bei! Breche auch im Satz um, wenn der Satz im Original in einer neuen Zeile weitergeht!"},
            {"type": "image_url", "image_url": {"url": image_url}}
        ]
    )
    if not model_vision:
        model_vision = ChatGroq(model=MODEL_NAME_VISION, api_key=os.getenv("GROQ_API_KEY"), temperature=0.0)         
    response = model_vision.invoke([aufgaben_message])
    with open(tdoc, "w") as f:
        f.writelines(response.content)



system_context="""
Scope: You are a high school teacher and have to grade class work.
Input: Input are one or more text documents, headed by <<TEXT_1>>...<<TEXT_N>>.
Output: Output is a single HTML document with headings TEXT_1..TEXT_N.

The document contains per TEXT a table A() with 2 columns. Both columns having the same width.
In the left column (AL) is the uncorrected original with all errors, the right column (AR) is the corrected version.

Correct and annotate in the right column (AR), but only colorize changed parts:
CRITERION_SPELLING_SPELLING: Upper and lower case, incorrect spelling. Annotate mistakes in red color.
CRITERION_SPELLING_PUNCTUATION: Period, comma and special characters, citation rules. Annotate mistakes in red color.
CRITERION_SPELLING_STRUCTURE: Grammar and incorrect or missing words. Annotate mistakes in red color.

Propose improvements in the right column (AR) in blue color:
CRITERION_CONTENT_STYLE: Readability and comprehensibility in the sentence and in the entire text.
CRITERION_CONTENT_CREATIVITY: Information content of the text.
CRITERION_CONTENT_SCOPE: Extent of the text.
CRITERION_CONTENT_QUESTIONS: Completeness of answers to the questions, if questions are asked by the teacher.

Per TEXT add a table (B) underneath with columns. Be polite in with the justification.
|Criterion|Possible Score|Achieved Score|Justification|
Sum up the points for CRITERION_SPELLING in the last row.
Sum up the points for CRITERION_CONTENT in the last row.


Calculate the score for the CRITERIONS in range 1..10 and consider all TEXT inputs to allow direct comparison.
Use the template here:
"""
# at the end and fit it to the number of input TEXT's. 

aufgaben_context="""
Language is british english. The children have been learning english for half a year. Consider this for the justification.


Task description:

You are on holiday with your family. You have a great house there. It's your dream house!

Write an email to your friend. Write about
- which rooms there are
- which things you can find there and what colour they are
- which room you like best
- what you do in your house

Write about ten sentences!

Here is the result to be evaluated:
"""

with open("data/template.html") as f:   
   template="".join(f.readlines())

print(template)
   

# Join alll input docs
exam_text=""
for i, doc in enumerate([doc+".txt" for doc in documents]):    
    tdoc=doc+".html"
    exam_text+=f"\n\n\n<<TEXT_{i+1}>>\n"
    with open(doc, "r", encoding="utf-8") as f:
        for line in f:
            print(line)
            exam_text += line

print(exam_text)
        
# Invoke model
messages = [
            ("system", system_context),
            # no f-string for parameters     
            ("user", f"{aufgaben_context}<<{{exam_text}}>>")            
]
        
prompt_template=ChatPromptTemplate.from_messages(messages=messages)      
user_input= {"exam_text": exam_text, "target_language": "English"}
# Use the formatted prompt with the model
if not model:
    model = ChatGroq(model=MODEL_NAME, api_key=os.getenv("GROQ_API_KEY"), temperature=0.0)
chain = prompt_template | model
response = chain.invoke(user_input)
with open("data/justification.html", "w", encoding="utf-8") as f:
    f.writelines(response.content)

        





