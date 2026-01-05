import streamlit as st
from PIL import Image, ImageFilter, ImageOps
import io

st.set_page_config(page_title="Fathi Media Tools", page_icon="🛠️", layout="centered")

st.title("🛠️ Fathi Media Tools")
st.caption("Tak perlu buka Canva. Upload, tukar saiz, download. Siap.")

# --- FUNGSI PROSES GAMBAR ---
def resize_with_blur(img, target_ratio=(9, 16)):
    # 1. Kira saiz baru
    width, height = img.size
    target_width = 1080
    target_height = 1920 # Default HD TikTok/Story
    
    # 2. Buat Background Blur
    # Resize gambar asal jadi besar sikit untuk cover background
    bg = img.resize((target_width, target_height))
    bg = bg.filter(ImageFilter.GaussianBlur(radius=50)) # Kasi kabur
    
    # 3. Letak Gambar Asal di Tengah
    # Kita pastikan gambar asal tak herot (maintain aspect ratio)
    img.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
    
    # Kira posisi tengah
    x = (target_width - img.width) // 2
    y = (target_height - img.height) // 2
    
    bg.paste(img, (x, y))
    return bg

# --- UI WEBSITE ---
tab1, tab2 = st.tabs(["📱 Auto-Fit TikTok/Story", "🔄 Converter Pantas"])

# TAB 1: UBAH SAIZ (RESIZE)
with tab1:
    st.header("Gambar AI → TikTok (9:16)")
    st.write("Masalah biasa: Gambar AI selalunya petak/melintang. Masuk TikTok jadi hitam atas bawah.")
    st.write("Alat ni akan tambah **'Blurry Background'** automatik.")
    
    uploaded_file = st.file_uploader("Upload Gambar (JPG/PNG)", type=['jpg', 'png', 'jpeg', 'webp'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Gambar Asal", use_container_width=True)
        
        if st.button("✨ Tukar Jadi Saiz Story/TikTok"):
            with st.spinner("Sedang memproses..."):
                # Proses gambar
                new_image = resize_with_blur(image)
                
                st.success("Siap!")
                st.image(new_image, caption="Hasil (Boleh terus post TikTok)", use_container_width=True)
                
                # Butang Download
                buf = io.BytesIO()
                new_image.save(buf, format="JPEG", quality=95)
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 Download Gambar Siap",
                    data=byte_im,
                    file_name="fathi_tiktok_ready.jpg",
                    mime="image/jpeg"
                )

# TAB 2: CONVERTER SIMPLE
with tab2:
    st.header("Penukar Format")
    st.write("Kadang-kadang download gambar format **.WEBP** tapi laptop/phone tak boleh baca. Tukar kat sini.")
    
    file_convert = st.file_uploader("Upload File Pelik", type=['webp', 'bmp', 'tiff'])
    
    if file_convert:
        img_c = Image.open(file_convert)
        st.image(img_c, caption="Gambar Preview", width=200)
        
        format_pilihan = st.radio("Tukar kepada:", ["JPEG (Ringan)", "PNG (Kualiti Tinggi)"])
        
        if st.button("Tukar Format"):
            buf_c = io.BytesIO()
            fmt = "JPEG" if "JPEG" in format_pilihan else "PNG"
            
            # Kalau JPEG kena convert mode ke RGB dulu (buang transparency)
            if fmt == "JPEG":
                img_c = img_c.convert("RGB")
                
            img_c.save(buf_c, format=fmt)
            byte_c = buf_c.getvalue()
            
            st.download_button(
                label=f"📥 Download sebagai {fmt}",
                data=byte_c,
                file_name=f"converted_image.{fmt.lower()}",
                mime=f"image/{fmt.lower()}"
            )
