import streamlit as st
import google.generativeai as genai

# Key tuan yang tadi
API_KEY = "AIzaSyDfgrEVdYtmL9QQyfo3dyQ4TYI_sKRsjcE"

st.set_page_config(page_title="Debug Fathi", page_icon="🔧")
st.title("🔧 Mode Cari Punca Masalah")

# UI Simple
ref = st.text_area("Teks Asal", "Test")
draft = st.text_area("Draft", "Test")

if st.button("Test Key Sekarang"):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("Hello, are you working?")
        
        st.success("✅ BERJAYA! Key berfungsi.")
        st.write(response.text)
        
    except Exception as e:
        st.error("❌ GAGAL. Ini punca sebenar (baca bawah):")
        # Ini akan tunjuk ayat penuh error dari Google
        st.code(str(e), language="bash")
        
        if "API has not been used" in str(e) or "Enable it" in str(e):
            st.warning("👉 PUNCA: Tuan belum tekan butang 'ENABLE' API. Sila ikut langkah Pilihan A di atas.")
        elif "Key not found" in str(e) or "API key not valid" in str(e):
            st.warning("👉 PUNCA: Key salah copy atau dah delete.")
