import streamlit as st

st.markdown('# Titulo!!!!')
st.markdown('## Subtitulo!!!!')
st.checkbox('Checkbox')
st.text_area('Text Area')
st.text_input('Text Input')
st.text('Lorem ipsum dolor sit amet, consectetur adipiscing elit')

import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [-12.046374, -77.042793],
    columns=['lat', 'lon'])

st.map(map_data)
