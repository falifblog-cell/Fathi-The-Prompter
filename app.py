import streamlit as st
import google.generativeai as genai

# --- SETUP ---
st.set_page_config(page_title="Fathi Ghostwriter Pro", page_icon="✍️", layout="wide")

st.title("✍️ Fathi Ghostwriter (Versi Stabil)")
st.caption("Masukkan gaya tulisan asal, AI akan tiru sebiji.")

# --- SIDEBAR: API KEY ---
with st.sidebar:
    st.header("🔑 Kunci AI")
    api_key = st.text_input("Paste Google API Key", type="password")
    st.info("Dapatkan key di: aistudio.google.com")
    st.warning("Pilih 'Create API key in NEW project' bila buat key.")

# --- FUNGSI AI (SAFE MODE) ---
def tulis_semula(key, rujukan, draf):
    # Setup
    genai.configure(api_key=key)
    
    # Kita guna 'gemini-pro' sebab dia paling stabil & jarang error version
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Bertindak sebagai penulis profesional. Tugas anda adalah menulis semula DRAF TEKS supaya mengikut GAYA RUJUKAN yang diberikan.
    
    ARAHAN PENTING (GAYA MANUSIA):
    1. Tiru nada (tone), penggunaan ganti nama (aku/kau/saya), dan slang dari RUJUKAN.
    2. Jangan guna perkataan skema AI (contoh: "kesimpulannya", "tambahan pula").
    3. Variasikan panjang ayat. Manusia suka campur ayat pendek dan panjang.
    
    ---
    GAYA RUJUKAN (TIRU INI):
    {rujukan}
    ---
    DRAF TEKS (ISI KANDUNGAN):
    {draf}
    ---
    """
    
    response = model.generate_content(prompt)
    return response.text

# --- ANTARA MUKA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Gaya Asal (Copy Paste tulisan lama)")
    ref_text = st.text_area("Contoh gaya penulisan tuan:", height=300, 
                            placeholder="Paste satu artikel lama tuan kat sini...")

with col2:
    st.subheader("2. Idea Baru (Draft Cincai)")
    draft_text = st.text_area("Apa point nak tulis hari ni?", height=300, 
                              placeholder="Contoh: Cerita pasal zaman ayah muda-muda, susah payah dulu...")

# --- BUTANG PROSES ---
st.divider()

if st.button("✨ Tulis Sekarang", type="primary"):
    if not api_key:
        st.error("Tuan belum masukkan API Key kat sebelah kiri.")
    elif not ref_text or not draft_text:
        st.warning("Isi dulu kotak Gaya Asal dan Idea Baru tu.")
    else:
        with st.spinner("Sedang menulis ikut gaya tuan..."):
            try:
                hasil = tulis_semula(api_key, ref_text, draft_text)
                st.success("Siap!")
                st.subheader("Hasil Tulisan:")
                st.write(hasil)
                st.code(hasil, language="text") # Senang copy
            except Exception as e:
                st.error(f"Ada masalah: {e}")
                st.caption("Jika error 404 keluar lagi, sila tekan 'Reboot App' di menu atas kanan.")
