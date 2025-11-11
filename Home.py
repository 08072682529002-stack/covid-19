#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st

st.set_page_config(page_title="Input Data", page_icon="📝", layout="wide")
st.title("📝 Input Data Pengguna")

# Input nama dan umur
st.session_state.nama = st.text_input("Nama Lengkap", value=st.session_state.get("nama", ""))
st.session_state.umur = st.number_input("Umur", min_value=1, max_value=120, value=st.session_state.get("umur", 20))

# Pilih gejala
st.subheader("🩺 Pilih Gejala yang Kamu Alami")
symptom_names = {
    'Kondisi Tubuh': 'Demam',
    'Batuk': 'Batuk Kering',
    'Lelah': 'Kelelahan',
    'Napas': 'Sesak Napas',
    'Tenggorokan': 'Sakit Tenggorokan',
    'Otot': 'Nyeri Otot',
    'Kepala': 'Sakit Kepala',
    'Pengecapan': 'Hilang Pengecapan',
    'Penciuman': 'Hilang Penciuman',
    'Diare': 'Diare',
}

selected = []
col1, col2 = st.columns(2)
items = list(symptom_names.items())
for i in range(0, len(items), 2):
    code1, name1 = items[i]
    with col1:
        if st.checkbox(name1, key=code1):
            selected.append(code1)
    if i + 1 < len(items):
        code2, name2 = items[i + 1]
        with col2:
            if st.checkbox(name2, key=code2):
                selected.append(code2)

st.session_state.gejala = selected

# Tombol lanjut
if st.button("➡️ Lanjut ke Diagnosis"):
    st.switch_page("pages/Hasil Diagnosis.py")


# In[ ]:




