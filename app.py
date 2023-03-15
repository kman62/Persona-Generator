import streamlit as st
import openai
import pandas as pd

# Set up the OpenAI API
openai.api_key = st.secrets['secrets']['openai_key']

# Define the function to generate the persona
def generate_persona(niche, location):
    # Generate the persona using OpenAI's GPT-3 API
    prompt = f"As an experienced digital marketing manager, you're tasked with creating a User persona for {niche} and {location}. Create the persona with the following details. DEMOGRAPHICS Name,Age,Occupation,Annual Income,Marital Status, Family Situation, Location USER DESCRIPTION: use the DEMOGRAPHICS data to create a user description PSYCHOGRAPHICS: Personal characteristics, Hobbies, Interests, Personal aspirations, Professional goals, Pains, Main challenges, Needs, Dreams SHOPPING BEHAVIORS: Budget, Shopping Frequency, Preferred channels, Online behavior, Search terms, Preferred brands, Triggers, Barriers. The output must be in a table format for each of the sections above. The table must have headings data points and answers. MUST Be in a table. Each row much have an answer."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=3000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Extract the persona data from the API response
    persona = response.choices[0].text
    persona = persona.split("\n")

    # Format the persona data as a Pandas DataFrame
    data = []
    for line in persona:
        if ":" in line:
            key, value = line.split(":")
            data.append([key.strip(), value.strip()])
    df = pd.DataFrame(data, columns=["Data Points", "Answers"])

    return df

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

