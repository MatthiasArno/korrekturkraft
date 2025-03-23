# See: https://docs.streamlit.io/develop/api-reference

# To view the results, open F1-"Simple Browse".
# Start the Webserver according to the output when running first time via debugger.
# In Settings, select "rerun on save".

#%% packages
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))
from pydantic import BaseModel
from langchain_core.output_parsers import SimpleJsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from pull_image import download_multiple_recipe_images

#%% Idea: 

# output
# { "recipe_name": "...", "ingredients": [{"name": "...", "quantity": ...}], "steps": []}


#%% define output format
class RecipeOutput(BaseModel):
    recipe_name: str
    ingredients: list[dict[str, str]]  # Change float to str for quantity
    steps: list[str]

    
# %% prompt template
messages = [
    ("system", "You are a recipe expert and deliver key information on specific recipes."),
    ("user", "Please provide key information on the recipe <<{recipe}>>. First translate everything into {language}. Return the result as JSON with the keys recipe_name, ingredients as list of dicts with keys name and quantity, steps as list of strings.")
]

prompt_template = ChatPromptTemplate.from_messages(messages=messages)
prompt_template

#%% model via Groq
MODEL_NAME = "llama3-8b-8192"
model = ChatGroq(model=MODEL_NAME)

#%% Chain definition
chain = prompt_template | model | StrOutputParser()| SimpleJsonOutputParser(pydantic_object=RecipeOutput)

#%% inference
# input_text = """
# Her er en opskrift på Spaghetti Carbonara:
# Du skal bruge 200 g spaghetti, 100 g bacon, 2 æg, 50 g parmesan og lidt peber.
# Kog spaghetti, steg bacon, bland æg og ost, og bland det hele med de varme nudler.
# """
# user_input = {"recipe": input_text, "language": "English"}
# res = chain.invoke(user_input)
# #%%
# res
# %%

import streamlit as st
from dotenv import load_dotenv, find_dotenv

st.title("Creative Dinning")

recipe_text=st.text_area(label="description", value="please add your recipe")
#recipe_text="300g Spaghetti, 500ml Tomate Sauce. Steps: cook the Spaghetti, mix with Sauce."

#st.button("Analyze", type="primary")
if st.button("Analyze",type="primary"):
    user_input = {"recipe": recipe_text, "language": "English"}
    res = chain.invoke(user_input)
    st.header(res["recipe_name"])
    col_left, col_right, col_edge=st.columns(3)

    results = download_multiple_recipe_images([res["recipe_name"]])

    with col_left:
        ingredients=res["ingredients"]
        count_ingredients=len(ingredients)
        st.subheader("Ingedients")
        for i in range(count_ingredients):
            st.write(f"name: {ingredients[i]['name']}, Quantity: {ingredients[i]['quantity']}")
    with col_right:
        st.subheader("Steps")
        st.write(res["steps"])
    with col_edge:
        st.subheader("hmm...")
        for recipe, path in results.items():
            st.image(path, caption='Optional image caption', use_column_width=True)
    
#	st.write("description", "ok,fried")



