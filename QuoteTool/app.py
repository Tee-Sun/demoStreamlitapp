import requests
import pandas as pd
import streamlit as st
from helpers import *
from ref import *


# Initiate Data App
st.title("Plan Quoting Tool")

st.markdown('')

#Set-up drag & drop input for csv upload into dataframe
file = st.file_uploader("Drop your census file here to load", type={"csv"})

#Upload file and return message when complete
try:
    inputs = pd.read_csv(file)
    st.text("Upload success!")
    data_js = inputs.to_json(orient='records')
    st.text(data_js)

except ValueError:
    st.text("Waiting for file...")


#Run Batch
@st.cache(suppress_st_warning=True)
def get_data(req, url, headers): #(x, rm, url, headers, threads)
    store = asyncio.run(async_batch_call(url, headers, req))
    z = write_results(store)
    return z

res = get_data(req, url, headers)
res_df = pd.json_normalize(res)
premium = res_df['Premium'].sum()
st.subheader('Annual Premium: :blue[${:0,.0f}]'.format(premium).replace('$-','-$'))




