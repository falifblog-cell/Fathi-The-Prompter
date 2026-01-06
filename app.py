import streamlit as st
import random

st.set_page_config(page_title="Fathi Style Enforcer", page_icon="📝", layout="wide")

st.title("📝 Fathi Style Enforcer (No AI)")
st.caption("Alat ini membetulkan ayat 'skema' jadi gaya 'Fathi' menggunakan logik bahasa semata-mata. 100% Zero AI.")

# --- DATA KAMUS GAYA FATHI (Boleh tambah lagi nanti) ---
# Ini adalah "Otak" manual dia. Kita ajar dia tukar perkataan baku.
kamus_gaya = {
    "saya": "aku",
    "anda": "korang",
    "tidak": "tak",
    "mahu": "nak",
    "kerana": "sebab",
    "tetapi": "tapi",
    "bagaimana": "macam mana",
    "mengapa": "kenapa",
    "sangat": "gila",
    "benar": "betul",
    "sedikit": "sikit",
    "melihat": "tengok",
    "berkata": "cakap",
    "sebenarnya": "actually",
    "contohnya": "contoh",
    "kemudian": "lepastu",
    "sekarang": "now",
    "mereka": "diorang",
    "terkejut": "tergamam",
    "kesimpulannya": "point dia,"
}

# --- TEMPLATE AYAT (Fill-in-the-blank) ---
# Ini memastikan struktur ayat sentiasa power macam writer pro.
templates = {
    "Intro Gempak": [
        "Jujur aku cakap, [TOPIK] ni memang nampak remeh. Tapi bila aku kaji balik...",
        "Ramai orang salah faham pasal [TOPIK]. Diorang ingat benda ni senang.",
        "Pernah tak korang rasa [TOPIK] tu macam tak masuk akal? Sama, aku pun dulu fikir macam tu."
    ],
    "Isi Penting": [
        "Benda paling mahal yang aku belajar ialah [POINT].",
        "Korang kena faham satu benda: [POINT]. Kalau tak faham ni, susah.",
        "Jangan buat [POINT] kalau korang belum ready nak hadap akibat dia."
    ],
    "Penutup/Call to Action": [
        "So, itu je aku nak pesan. Terpulang kat korang nak percaya ke tak.",
        "Kalau korang rasa benda ni manfaat, tolonglah [ACTION]. Jangan simpan sorang.",
        "Akhir kata, [ACTION] sekarang sebelum terlambat."
    ]
}

# --- FUNGSI TUKAR BAHASA ---
def tukar_gaya_fathi(teks):
    words = teks.split()
    new_words = []
    count_tukar = 0
    
    for word in words:
        # Bersihkan tanda baca sikit (koma/titik)
        clean_word = word.lower().strip(".,!?")
        
        if clean_word in kamus_gaya:
            gantian = kamus_gaya[clean_word]
            # Kekalkan huruf besar kalau asal huruf besar
            if word[0].isupper():
                gantian = gantian.capitalize()
            # Tambah balik tanda baca
            if word.endswith(","): gantian += ","
            elif word.endswith("."): gantian += "."
            elif word.endswith("?"): gantian += "?"
            
            new_words.append(f"**{gantian}**") # Bold kan perkataan yang ditukar
            count_tukar += 1
        else:
            new_words.append(word)
            
    return " ".join(new_words), count_tukar

# --- UI WEBSITE ---
tab1, tab2 = st.tabs(["🔄 Tukar Skema -> Santai", "📋 Template Menulis"])

# TAB 1: AUTO CONVERT
with tab1:
    st.header("Penukar Bahasa Baku")
    st.write("Masukkan teks skema (macam ChatGPT tulis), app ni akan 'kasarkan' sikit jadi bahasa Fathi.")
    
    input_text = st.text_area("Teks Asal (Skema):", height=150, placeholder="Contoh: Saya tidak mahu melakukan perkara itu kerana ia sangat susah.")
    
    if st.button("Tukar Gaya!"):
        if input_text:
            hasil, jumlah = tukar_gaya_fathi(input_text)
            st.success(f"Siap! Ada {jumlah} perkataan telah diubah.")
            st.markdown(hasil) # Markdown supaya boleh nampak bold
            
            st.code(hasil.replace("**", ""), language="text") # Teks bersih untuk copy
        else:
            st.warning("Masukkan teks dulu.")

# TAB 2: TEMPLATE VAULT
with tab2:
    st.header("Bank Ayat Power")
    st.write("Tak ada idea nak mula? Pilih je template ni.")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        jenis = st.selectbox("Nak tulis bahagian mana?", ["Intro Gempak", "Isi Penting", "Penutup/Call to Action"])
        # Input pembolehubah
        variable = ""
        if jenis == "Intro Gempak": variable = st.text_input("Topik apa?", placeholder="Contoh: AI Writer")
        elif jenis == "Isi Penting": variable = st.text_input("Apa Point Utama?", placeholder="Contoh: konsistensi itu kunci")
        elif jenis == "Penutup/Call to Action": variable = st.text_input("Nak suruh buat apa?", placeholder="Contoh: share post ni")
    
    with col_b:
        st.subheader("Hasil:")
        if variable:
            pilihan = templates[jenis]
            for ayat in pilihan:
                # Ganti placeholder [TOPIK] dengan input user
                final_ayat = ayat.replace("[TOPIK]", f"*{variable}*").replace("[POINT]", f"*{variable}*").replace("[ACTION]", f"*{variable}*")
                st.info(final_ayat)
                if st.button("Copy", key=ayat):
                    st.toast("Ayat dicopy! (Simulasi)")
        else:
            st.warning("Isi kotak sebelah kiri dulu.")
