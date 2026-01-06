import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="Fathi's Ghostwriter (Gemini)", page_icon="✍️", layout="wide")

st.title("✍️ Fathi's Ghostwriter (Edisi Gemini)")
st.caption("Guna AI Google (Percuma) untuk tiru gaya tulisan anda.")

# --- SIDEBAR: API KEY ---
with st.sidebar:
    st.header("Setting")
    api_key = st.text_input("Masukkan Google API Key", type="password", help="Dapatkan free di aistudio.google.com")
    
    # Model Gemini yang laju dan percuma
    model_pilihan = st.selectbox("Model", ["gemini-1.5-flash", "gemini-1.5-pro"], index=0)
    
    st.divider()
    st.info("Tips: Masukkan contoh tulisan anda yang paling 'human' (banyak slang, emosi, atau ayat pendek).")

# --- MAIN AREA ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Gaya Rujukan (Reference)")
    ref_text = st.text_area("Paste tulisan lama anda di sini:", height=300, 
                            placeholder="Contoh: 'Aku sebenarnya malas nak tulis panjang. Tapi bila fikir balik, benda ni penting...'")

with col2:
    st.subheader("2. Draft / Point Baru")
    draft_text = st.text_area("Apa yang nak ditulis sekarang?", height=300, 
                              placeholder="Point: \n- AI makin power\n- Kita kena adapt\n- Jangan takut teknologi")

# --- THE "SECRET SAUCE" PROMPT (GEMINI VERSION) ---
def humanize_text_gemini(api_key, model_name, reference, draft):
    # Setup Gemini
    genai.configure(api_key=api_key)
    
    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    }
    
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction="You are a professional Ghostwriter. Your ONLY task is to rewrite the input text to match a specific reference style."
    )
    
    prompt_rahsia = f"""
    Please rewrite the 'DRAFT TEXT' below. You must STRICTLY mimic the writing style, tone, vocabulary, and sentence structure of the 'REFERENCE TEXT'.
    
    CRITICAL INSTRUCTIONS FOR HUMAN-LIKE WRITING:
    1. **Analyze the Reference:** Look for 'burstiness' (mix of very short and long sentences). Does the writer use slang (Bahasa Pasar)? Is the tone sarcastic or serious?
    2. **Mimic the Imperfections:** Do not write perfectly. Humans make casual transitions. Avoid robotic words like "Kesimpulannya" or "Tambahan pula". Use natural connectors like "So,", "Lagipun,", "Btw," if the reference uses them.
    3. **Language:** If the reference is in Malay/Rojak, the output MUST be in Malay/Rojak.
    
    ---
    REFERENCE TEXT (STYLE TO COPY):
    {reference}
    ---
    DRAFT TEXT (CONTENT TO REWRITE):
    {draft}
    ---
    """
    
    response = model.generate_content(prompt_rahsia)
    return response.text

# --- ACTION BUTTON ---
st.divider()

if st.button("✨ Tulis Semula (Guna Gemini)", type="primary"):
    if not api_key:
        st.warning("Sila masukkan Google API Key kat tepi tu dulu.")
    elif ref_text and draft_text:
        with st.spinner("Gemini sedang memproses gaya otak anda..."):
            try:
                hasil = humanize_text_gemini(api_key, model_pilihan, ref_text, draft_text)
                
                st.subheader("📝 Hasil Tulisan:")
                st.write(hasil)
                
                st.divider()
                st.code(hasil, language="text") # Senang copy
                st.success("Siap!")
                
            except Exception as e:
                st.error(f"Error: {e} (Mungkin API Key salah atau kuota free dah habis limit per minit)")
    else:
        st.warning("Sila isi kedua-dua kotak rujukan dan draft.")
