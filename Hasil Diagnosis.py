#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hasil Diagnosis", page_icon="🧪", layout="wide")
st.title("🧪 Hasil Diagnosis COVID-19")

# Basis pengetahuan
knowledge_base = {
    'Kondisi Tubuh': {'COVID-19': 0.8, 'theta': 0.2},
    'Batuk': {'COVID-19': 0.7, 'theta': 0.3},
    'Lelah': {'COVID-19': 0.6, 'theta': 0.4},
    'Napas': {'COVID-19': 0.9, 'theta': 0.1},
    'Tenggorokan': {'COVID-19': 0.5, 'theta': 0.5},
    'Otot': {'COVID-19': 0.4, 'theta': 0.6},
    'Kepala': {'COVID-19': 0.3, 'theta': 0.7},
    'Pengecapan': {'COVID-19': 0.9, 'theta': 0.1},
    'Penciuman': {'COVID-19': 0.9, 'theta': 0.1},
    'Diare': {'COVID-19': 0.2, 'theta': 0.8},
}

def combine_mass(m1, m2):
    possible_hypotheses = set(['COVID-19', 'theta'])
    new_mass = {}
    conflict_k = 0
    for h1_str, val1 in m1.items():
        for h2_str, val2 in m2.items():
            h1 = set(h1_str.split(',')) if h1_str != 'theta' else possible_hypotheses
            h2 = set(h2_str.split(',')) if h2_str != 'theta' else possible_hypotheses
            intersection = h1.intersection(h2)
            if not intersection:
                conflict_k += val1 * val2
                continue
            new_h_str = ','.join(sorted(list(intersection)))
            if new_h_str == 'COVID-19,theta':
                new_h_str = 'theta'
            new_mass[new_h_str] = new_mass.get(new_h_str, 0) + (val1 * val2)
    if conflict_k == 1:
        return {'theta': 1.0}
    denominator = 1 - conflict_k
    return {h: val / denominator for h, val in new_mass.items()}

# Ambil data dari session
nama = st.session_state.get("nama", "")
umur = st.session_state.get("umur", 0)
gejala = st.session_state.get("gejala", [])

if not nama or not umur or not gejala:
    st.warning("⚠️ Data belum lengkap. Silakan kembali ke halaman input.")
    st.page_link("Home.py", label="⬅️ Kembali ke Input")
else:
    if len(gejala) == 1:
        result_mass = knowledge_base[gejala[0]]
    else:
        result_mass = knowledge_base[gejala[0]]
        for i in range(1, len(gejala)):
            result_mass = combine_mass(result_mass, knowledge_base[gejala[i]])

    belief_covid = result_mass.get('COVID-19', 0)
    belief_theta = result_mass.get('theta', 0)

    st.metric("🧪 Keyakinan COVID-19", f"{belief_covid * 100:.2f}%")
    st.progress(belief_covid)
    st.metric("❔ Ketidaktahuan (Theta)", f"{belief_theta * 100:.2f}%")
    st.progress(belief_theta)

    if belief_covid > 0.8:
        kesimpulan = "🟢 Sangat Yakin terdiagnosis COVID-19."
        st.success(kesimpulan)
    elif belief_covid > 0.5:
        kesimpulan = "🟡 Cukup Yakin terdiagnosis COVID-19."
        st.warning(kesimpulan)
    else:
        kesimpulan = "🔴 Tidak Cukup Bukti untuk terdiagnosis COVID-19."
        st.error(kesimpulan)

    # Simpan riwayat
    df = pd.DataFrame([{
        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nama": nama,
        "Umur": umur,
        "Gejala": ', '.join(gejala),
        "Belief COVID-19": f"{belief_covid:.2f}",
        "Theta": f"{belief_theta:.2f}",
        "Kesimpulan": kesimpulan
    }])
    df.to_csv("riwayat_diagnosis.csv", mode="a", header=False, index=False, encoding="utf-8")

    st.page_link("pages/Riwayat.py", label="📜 Lihat Riwayat Diagnosis")
    st.page_link("Home.py", label="🔄 Isi Ulang Form")


# In[ ]:
