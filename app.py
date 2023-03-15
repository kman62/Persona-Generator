import streamlit as st
import openai
import pandas as pd

# Set up the OpenAI API
openai.api_key = st.secrets['secrets']['openai_key']

# Define the function to generate the persona
def generate_persona(niche, location):
    # rest of the code

# Define the Streamlit app
st.set_page_config(page_title="Persona Generator", page_icon=":smiley:")
st.title("Buyer Persona Generator")

with st.form(key="persona_form"):
    st.write("Enter the following information to generate the buyer persona:")
    niche = st.text_input("Niche")
    location = st.text_input("Location")
    submit_button = st.form_submit_button(label="Generate Persona")

if submit_button:
    persona = generate_persona(niche, location)

    st.header("DEMOGRAPHICS")
    st.table(persona[persona["Data Points"].str.contains("Name|Age|Occupation|Annual Income|Marital Status|Family Situation|Location")])

    st.header("USER DESCRIPTION")
    st.table(persona[persona["Data Points"].str.contains("User Description")])

    st.header("PSYCHOGRAPHICS")
    st.table(persona[persona["Data Points"].str.contains("Personal characteristics|Hobbies|Interests|Personal aspirations|Professional goals|Pains|Main challenges|Needs|Dreams")])

    st.header("SHOPPING BEHAVIORS")
    st.table(persona[persona["Data Points"].str.contains("Budget|Shopping Frequency|Preferred channels|Online behavior|Search terms|Preferred brands|Triggers|Barriers")])
