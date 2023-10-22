import streamlit as st
from code_editor import code_editor

response_dict = code_editor(your_code_string)

code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language='python')
