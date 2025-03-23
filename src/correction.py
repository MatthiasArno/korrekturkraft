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

        





