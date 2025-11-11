#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Riwayat Diagnosis", page_icon="📜", layout="wide")
st.title("📜 Riwayat Diagnosis COVID-19")

if os.path.exists("riwayat_diagnosis.csv"):
    df = pd.read_csv("riwayat_diagnosis.csv", header=None, encoding="utf-8")
    df.columns = ["Waktu", "Nama", "Umur", "Gejala", "Belief COVID-19", "Theta", "Kesimpulan"]
    st.dataframe(df, height=400)
else:
    st.info("Belum ada riwayat diagnosis yang tersimpan.")



# In[ ]:
