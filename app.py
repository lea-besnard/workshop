import pandas as pd
import streamlit as st
from streamlit import write
from transformers import pipeline
import osfrom google.cloud import firestore

def app():
    
    unmasker = pipeline('fill-mask', model='./distilbert-base-uncased')
    sentence = st.text_input('Fill in the sentence you want to try then press enter:', 'Data science is [MASK].')
    if "[MASK]" in sentence:
        result = unmasker(sentence)
        st.write(pd.DataFrame(result))
    else:
        st.warning("Léa is the best")
       
    if st.button("Store result in the database"):
        db = firestore.Client.from_service_account_info(st.secrets["gcp_service_account"])
        data = {
            u"table_results": result
        }
        db.collection("posts").document(sentence).set(data)

if __name__ == '__main__':

    app()
    
