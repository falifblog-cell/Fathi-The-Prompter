import streamlit as st
import google.generativeai as genai

# --- KUNCI DITANAM TERUS (JANGAN SHARE KOD NI DENGAN ORANG LAIN) ---
API_KEY = "AIzaSyDfgrEVdYtmL9QQyfo3dyQ4TYI_sKRsjcE"

# --- SETUP ---
st.set_page_config(page_title="Fathi Ghostwriter (Direct)", page_icon="📝", layout="wide")

st.title("📝 Fathi Ghostwriter (Siap Sedia)")
st.caption("Tak payah masuk key. Masukkan idea, terus jalan.")

# --- FUNGSI 'JALA IKAN' (AUTO-DETECT MODEL) ---
def tulis_guna_sebarang_model(key, rujukan, draf):
    genai.configure(api_key=key)
    
    # Kita suruh dia try semua model sampai jumpa yang boleh
    senarai_model = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    
    prompt = f"""
    Bertindak sebagai penulis profesional. Tulis semula DRAF TEKS supaya mengikut GAYA RUJUKAN.
    
    ARAHAN:
    1. Tiru nada (tone), slang, dan ganti nama (aku/kau/saya) dari rujukan.
    2. Jangan guna bahasa skema/baku sangat.
    3. Variasikan panjang ayat (pendek & panjang).
    
    STYLE: {rujukan}
    CONTENT: {draf}
    """
    
    error_log = []
    
    for nama_model in senarai_model:
        try:
            # Cuba model ni
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text, nama_model # Berjaya!
        except Exception:
            # Gagal, try next one
            error_log.append(f"{nama_model} gagal")
            continue
            
    return None, str(error_log)

# --- UI ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Gaya Asal")
    ref_text = st.text_area("Contoh tulisan lama:", height=300, 
                            placeholder="Paste artikel lama yang awak suka gayanya...")

with col2:
    st.subheader("2. Idea Baru")
    draft_text = st.text_area("Point nak tulis:", height=300, 
                              placeholder="Cerita pasal...")

st.divider()

if st.button("✨ Tulis Sekarang", type="primary"):
    if ref_text and draft_text:
        with st.spinner("Sedang menulis..."):
            hasil, info = tulis_guna_sebarang_model(API_KEY, ref_text, draft_text)
            
            if hasil:
                st.success(f"Siap! (Guna model: {info})")
                st.markdown(hasil)
                st.divider()
                st.code(hasil, language="text")
            else:
                st.error("Masalah besar: Key ni mungkin salah atau belum aktif.")
    else:
        st.warning("Isi kotak teks dulu bos.")
