from dotenv import load_dotenv, find_dotenv
import base64
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import os


MODEL_NAME_VISION = "llama-3.2-11b-vision-preview"
model_vision = None

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
