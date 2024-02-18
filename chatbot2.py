import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import openai
import json
import os
from dotenv import load_dotenv,find_dotenv

# Load environment variables from .env file
load_dotenv()
_ = load_dotenv(find_dotenv())

# Set your OpenAI GPT-3.5 API key from the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")
# Application title and body
st.set_page_config(page_title="ASK HIM", page_icon="", layout='wide')

# Title of application
st.title("ASK HIM")

# Page Structure
with st.sidebar:
    st.title("ASK HIM")
    st.markdown('''
        ### 
        Designed By Oduyebo oluwuatobi victor
    ''', unsafe_allow_html=True)

# Session State
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["Hi, I'm Ask Him. How can I assist you today?"]
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hello!']

# Application layout
input_container = st.container()
response_container = st.container()

# User inputs
def get_text():
    input_text = st.text_input("Text here to ask me...", "", key="input")
    return input_text

# Applying the user input box
with input_container:
    user_input = get_text()
    
    
# Function to crop image in circular shape
def crop_to_circle(image):
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    result = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result

# Loading and cropping the user's profile image
profile_image = Image.open("6be71193-3046-4e96-a6a9-f9cd01b0bd7a.JPG")
profile_image = crop_to_circle(profile_image)

# Displaying the cropped profile image
st.sidebar.image(profile_image, use_column_width=True)

# Bot outputs
def generate_response(prompt):
    # Use ChatCompletion for interactive conversations
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content'].strip()

with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            st.write("💬 User:", st.session_state['past'][i])
            st.write("💡 Tobi:", st.session_state['generated'][i])

# Save chat history to a file
with open("chat_history.json", "w") as file:
#     json.dump(st.session_state['chat_history'], file)
# Session State
     if 'generated' not in st.session_state:
      st.session_state['generated'] = ["Hi, I'm Ask Him. How can I assist you today?"]
     if 'past' not in st.session_state:
      st.session_state['past'] = ['Hello!']
     if 'chat_history' not in st.session_state:
      st.session_state['chat_history'] = []
