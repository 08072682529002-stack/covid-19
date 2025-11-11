#!/usr/bin/env python
# coding: utf-8

# In[1]:

import streamlit as st
from datetime import datetime

# Konfigurasi halaman
st.set_page_config(page_title="Diagnosis COVID-19", page_icon="🦠", layout="wide")

# Basis Pengetahuan
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

possible_hypotheses = set(['COVID-19', 'theta'])

# Fungsi Dempster-Shafer
def combine_mass(m1, m2):
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
        st.error("❌ Terjadi konflik total antar bukti.")
        return {'theta': 1.0}
    denominator = 1 - conflict_k
    return {h: val / denominator for h, val in new_mass.items()}

# Tampilan Header
st.markdown("""
<div style='
    background-color: #f0f8ff;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #d0d0d0;
    display: flex;
    align-items: center;
    gap: 1rem;
'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/SARS-CoV-2_without_background.png/220px-SARS-CoV-2_without_background.png' width='60'>
    <div>
        <h2 style='margin-bottom: 0;'>🦠 Sistem Pakar Diagnosis COVID-19</h2>
        <p style='margin-top: 5px; font-size: 16px; color: #333;'>Cepat • Akurat • Informatif</p>
    </div>
</div>
""", unsafe_allow_html=True)


# Input Data Pengguna
st.subheader("🧑‍⚕️ Data Pengguna")
nama = st.text_input("Nama Lengkap")
umur = st.number_input("Umur", min_value=0, max_value=120, step=1)

# Pilih Gejala
st.subheader("🩺 Pilih Gejala yang Kamu Alami")
selected_symptoms_map = {}
col1, col2 = st.columns(2)
items = list(symptom_names.items())
for i in range(0, len(items), 2):
    code1, name1 = items[i]
    with col1:
        selected_symptoms_map[code1] = st.checkbox(f"✅ {name1}")
    if i + 1 < len(items):
        code2, name2 = items[i + 1]
        with col2:
            selected_symptoms_map[code2] = st.checkbox(f"✅ {name2}")

st.markdown("---")
process_button = st.button("🚀 Proses Diagnosis")

# Proses Diagnosis
if process_button:
    selected_symptoms_list = [code for code, selected in selected_symptoms_map.items() if selected]
    gejala_terpilih = [symptom_names[c] for c in selected_symptoms_list]

    if not nama or umur == 0:
        st.warning("⚠️ Silakan isi nama dan umur terlebih dahulu.")
    elif not selected_symptoms_list:
        st.warning("⚠️ Silakan pilih minimal tiga gejala.")
    else:
        # Hitung keyakinan
        if len(selected_symptoms_list) == 3:
            result_mass = knowledge_base[selected_symptoms_list[0]]
        else:
            result_mass = knowledge_base[selected_symptoms_list[0]]
            for i in range(1, len(selected_symptoms_list)):
                m2 = knowledge_base[selected_symptoms_list[i]]
                result_mass = combine_mass(result_mass, m2)

        belief_covid = result_mass.get('COVID-19', 0)
        belief_theta = result_mass.get('theta', 0)

        # Tampilkan hasil
        st.markdown("### 📊 Hasil Diagnosis")
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

        # Detail tambahan
        st.markdown("### 🧾 Detail Diagnosis")
        st.info(f"🕒 Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.info(f"👤 Nama: {nama} | Umur: {umur} tahun")
        st.info(f"🩺 Gejala: {', '.join(gejala_terpilih)}")

        # Saran Kesehatan
        st.markdown("### 🩺 Saran Kesehatan")
        if belief_covid > 0.8:
            st.info("""
            ✅ **Saran:**  
            - Tes PCR/antigen segera  
            - Isolasi mandiri 5–7 hari  
            - Konsumsi makanan bergizi  
            - Hubungi tenaga medis jika gejala berat
            """)
        elif belief_covid > 0.5:
            st.info("""
            ⚠️ **Saran:**  
            - Lakukan tes COVID-19 untuk konfirmasi  
            - Pantau gejala selama 3 hari  
            - Gunakan masker saat beraktivitas  
            - Istirahat cukup dan minum air putih
            """)
        else:
            st.info("""
            🛡️ **Saran:**  
            - Tetap jaga protokol kesehatan  
            - Perkuat imun dengan makanan sehat  
            - Hindari kerumunan  
            - Lakukan pemeriksaan jika muncul gejala baru
            """)



# In[ ]:




