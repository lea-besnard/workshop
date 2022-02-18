import pandas as pd
import streamlit as st
from streamlit import write
from transformers import pipeline
import os
from google.cloud import firestore

def app():
    
    unmasker = pipeline('fill-mask', model='./distilbert-base-uncased')
    sentence = st.text_input('Fill in the sentence you want to try then press enter:', 'Data science is [MASK].')
    if "[MASK]" in sentence:
        result = unmasker(sentence)
        st.write(pd.DataFrame(result))
    else:
        st.warning("Léa is the best")
    db = firestore.Client.from_service_account_info(st.secrets["gcp_service_account"])
    if st.button("Store result in the database"):
        data = {
            u"table_results": result
        }
        db.collection("posts").document(sentence).set(data)
        
   
    docs = db.collection(u'posts').stream()
    sentences = []
    for doc in docs:
        sentences.append(doc.id)
    selected_sentence = st.selectbox("Select a stored sentence to look at the result", sentences)
    table = db.collection(u'posts').document(selected_sentence).get().to_dict()["table_results"]
    st.write(pd.DataFrame(table))

if __name__ == '__main__':

    app()
    
