import streamlit as st

st.set_page_config(page_title="Fathi Prompt Builder", page_icon="🎨", layout="wide")

st.title("🎨 Mesin Pembuat Prompt Fathi")
st.caption("Klik-klik je, terus siap prompt power untuk Midjourney/Dall-E.")

# --- BAHAGIAN KIRI: INPUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Subjek Utama")
    subjek = st.text_area("Apa yang nak dilukis?", height=100, placeholder="Contoh: A Japanese soldier holding a bicycle in Kota Bharu beach...")
    
    st.subheader("2. Gaya & Suasana (Vibe)")
    # Pilihan gaya yang awak selalu guna
    style = st.selectbox("Gaya Seni:", 
                         ["Cinematic Reality (Macam Filem)", "Vintage 1940s Photo", "Oil Painting", "Anime Style", "Sketch/Drawing"])
    
    lighting = st.select_slider("Pencahayaan:", 
                                options=["Dull/Overcast", "Natural Sunlight", "Golden Hour (Senja)", "Dark/Moody", "Neon Lights"])
    
    camera = st.selectbox("Sudut Kamera:", 
                          ["Eye Level (Biasa)", "Low Angle (Nampak Gah)", "Drone View (Dari Atas)", "Close Up (Muka Sahaja)", "Wide Angle (Pemandangan Luas)"])

with col2:
    st.subheader("3. Perincian Teknikal")
    
    # Checkbox untuk tambah 'perasa'
    st.write("Tambah Elemen Extra:")
    kualiti = st.checkbox("High Quality keywords (8k, masterpiece, sharp focus)", value=True)
    no_blur = st.checkbox("Anti-Blur (depth of field, detailed background)")
    
    # Aspect Ratio (Midjourney style)
    ratio = st.radio("Saiz Gambar (--ar):", ["16:9 (Landscape)", "9:16 (TikTok/Story)", "1:1 (Square)", "4:5 (Instagram)"])
    
    # Versi Midjourney
    version = st.radio("Versi Enjin (--v):", ["6.0", "5.2", "Niji (Anime)"])

# --- BAHAGIAN BAWAH: HASIL ---
st.divider()
st.header("✨ Hasil Prompt Anda")

# Logic gabung ayat
prompt_text = f"{subjek}, {style}, {lighting} lighting, {camera} shot"

if kualiti:
    prompt_text += ", 8k resolution, masterpiece, highly detailed, sharp focus"
if no_blur:
    prompt_text += ", detailed background, no blur"

# Format teknikal Midjourney
ar_code = ratio.split("(")[0].strip() # Ambil nombor je, buang teks dalam kurungan
v_code = version.split("(")[0].strip()

final_prompt = f"/imagine prompt: {prompt_text} --ar {ar_code} --v {v_code}"

# Paparan kod yang cantik
st.code(final_prompt, language="markdown")

st.info("👆 Tekan ikon 'Copy' kecil kat bucu kanan kotak di atas, lepas tu paste kat Discord/Bing.")
