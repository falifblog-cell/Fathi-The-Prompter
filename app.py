import streamlit as st
import google.generativeai as genai

# --- SETUP ---
st.set_page_config(page_title="Fathi Ghostwriter (Auto-Fix)", page_icon="🤖", layout="wide")

st.title("🤖 Fathi Ghostwriter (Auto-Detect)")
st.caption("Versi ini akan cari sendiri model AI yang 'hidup' dalam API Key tuan.")

# --- SIDEBAR ---
with st.sidebar:
    api_key = st.text_input("Paste Google API Key", type="password")
    st.info("Key dari: aistudio.google.com")

# --- FUNGSI 'JALA IKAN' (TRY ALL MODELS) ---
def tulis_guna_sebarang_model(key, rujukan, draf):
    genai.configure(api_key=key)
    
    # Senarai model yang kita akan cuba satu-persatu
    senarai_model = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro", "gemini-1.0-pro"]
    
    prompt = f"""
    Tulis semula teks ini mengikut gaya rujukan.
    STYLE: {rujukan}
    CONTENT: {draf}
    """
    
    error_log = []
    
    # Loop: Cuba model pertama, kalau gagal, cuba kedua...
    for nama_model in senarai_model:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text, nama_model # Berjaya! Pulangkan teks & nama model
        except Exception as e:
            error_log.append(f"{nama_model}: Gagal")
            continue # Try model seterusnya
            
    # Kalau semua gagal
    return None, str(error_log)

# --- UI ---
col1, col2 = st.columns(2)
with col1:
    ref_text = st.text_area("Gaya Asal:", height=200, placeholder="Paste tulisan lama...")
with col2:
    draft_text = st.text_area("Idea Baru:", height=200, placeholder="Nak tulis apa...")

if st.button("✨ Tulis Sekarang (Auto-Detect)", type="primary"):
    if api_key and ref_text and draft_text:
        with st.spinner("Sedang mencari model AI yang sesuai..."):
            hasil, info = tulis_guna_sebarang_model(api_key, ref_text, draft_text)
            
            if hasil:
                st.success(f"Berjaya! Menggunakan model: {info}")
                st.write(hasil)
                st.code(hasil, language="text")
            else:
                st.error("Semua model gagal. Masalah mungkin pada API Key.")
                st.error(f"Log Error: {info}")
    else:
        st.warning("Isi semua kotak dulu.")
