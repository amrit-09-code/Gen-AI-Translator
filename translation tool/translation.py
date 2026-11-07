import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="GenAI Translator Tool", page_icon="🌐", layout="centered")
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
st.markdown("""
<style>
    .stApp {
        background:linear-gradient(135deg,#eef2ff 0%,#f8f9ff 100%);
    }
    .stTextInput input,.stSelectbox div[data-baseweb="select"]{
      border-radius:12px;
      border:2px solid #d1d5db;
      background-color:#f9fafb;
    }
      
    .stButton button{
      background:linear-gradient(90deg,#10b981,#06b6d4);
      color:white;
      border-radius:12px;
      width:100%;
      font-weight:600;
      border:none;
      padding:10px;
      box-shadow:0 5px 15px rgba(16,185,129,0.5);
    }
    .stButton button:hover{
      transform:scale(1.05);
      background:linear-gradient(90deg,#06b6d4,#10b981);
    }
    h1{
      background:linear-gradient(90deg,#667eea,#764ba2);
      color:#0066FF;
      text-align: center;
    }

</style>
""",unsafe_allow_html=True)
st.title("GenAI Translator Tool🌐")
text = st.text_input("Enter Your Text")
language = st.selectbox("Select Language", ["Hindi", "English", "French", "Spanish", "Punjabi"])

if st.button("Translate"):
    if not text.strip():
        st.warning("Please enter text")
    elif client is None:
        st.error("GOOGLE_API_KEY is missing. Add it to your .env file.")
    else:
        
        models_to_try = ["gemini-3.8-flash", "gemini-3.5-flash"]
        response = None
        translation_successful = False
        
        with st.spinner("Translating..."):
            for current_model in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=current_model,
                        contents=f"Translate to {language}: {text}"
                    )
                    if response and response.text:
                        st.success(response.text)
                        translation_successful = True
                        break  
                except Exception as model_error:
                    
                    if "503" in str(model_error) or "UNAVAILABLE" in str(model_error):
                        continue
                    else:
                        st.error(f"Translation failed: {model_error}")
                        translation_successful = True
                        break
                        
        if not translation_successful:
            st.error("Google's servers are facing exceptionally high traffic right now. Please wait a few seconds and try again.")
