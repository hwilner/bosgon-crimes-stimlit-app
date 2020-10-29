import streamlit as st
import pandas as pd

import numpy as np

print(5)


@st.cache
def load_df():
    # Make sure to place the right path to you csv
    df = pd.read_csv('crime.csv', encoding='unicode_escape')

    df = df.rename(columns={

        'Lat': 'lat',
        'Long': 'lon'
    })
    df = df.dropna(subset=['lat', 'lon'])

    np.random.seed(40001)

    coords_mask = df['lat'] > 40
    return df[coords_mask].sample(n=20000)