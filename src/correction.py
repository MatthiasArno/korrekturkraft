from dotenv import load_dotenv, find_dotenv
import base64
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import os

try:
    load_dotenv(find_dotenv(usecwd=True))
except:
   pass

os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
model = None

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

task_context="""
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


def run_correction(template, list_of_files:dict, system_context, task_context):

    exam_text=""
    for name, text in list_of_files.items(): 
        exam_text+=f"\n\n\n<<TEXT:{name}>>\n"
        exam_text += text

        
    # Invoke model
    messages = [
                ("system", system_context+"\n"+template),
                # no f-string for parameters     
                ("user", f"{task_context}<<{{exam_text}}>>")            
    ]
            
    prompt_template=ChatPromptTemplate.from_messages(messages=messages)      
    user_input= {"exam_text": exam_text, "target_language": "English"}
    # Use the formatted prompt with the model
    model=None
    if not model:
        model = ChatGroq(model=MODEL_NAME, api_key=os.getenv("GROQ_API_KEY"), temperature=0.0)
    chain = prompt_template | model
    response = chain.invoke(user_input)
    return response.content

        





