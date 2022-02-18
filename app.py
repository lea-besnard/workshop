import pandas as pd
import streamlit as st
from streamlit import write
from transformers import pipeline
import os

def app():
    
    unmasker = pipeline('fill-mask', model='./distilbert-base-uncased')
    sentence = st.text_input('Fill in the sentence you want to try then press enter:', 'Data science is [MASK].')
    if "[MASK]" in sentence:
        result = unmasker(sentence)
        st.write(pd.DataFrame(result))
    else:
        st.warning("The sentence needs to contains [MASK]")


if __name__ == '__main__':

    app()
    
