import streamlit as st
from openai import OpenAI

# --- CONFIGURATION ---
st.set_page_config(page_title="Fathi's Ghostwriter", page_icon="✍️", layout="wide")

st.title("✍️ Fathi's Ghostwriter (Anti-AI Detector)")
st.caption("App ini akan meniru gaya penulisan asal anda supaya hasil nampak 100% manusia.")

# --- SIDEBAR: API KEY ---
with st.sidebar:
    st.header("Setting")
    api_key = st.text_input("Masukkan OpenAI API Key", type="password", help="Dapatkan di platform.openai.com")
    if not api_key:
        st.warning("Sila masukkan API Key untuk mula.")
        st.stop()
    
    model_pilihan = st.selectbox("Model AI", ["gpt-4o", "gpt-4-turbo"], index=0, help="GPT-4o paling pandai tiru gaya bahasa.")
    
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

# --- THE "SECRET SAUCE" PROMPT ---
def humanize_text(client, reference, draft):
    prompt_rahsia = f"""
    You are a professional Ghostwriter. Your task is to rewrite the 'DRAFT TEXT' to strictly match the writing style, tone, and vocabulary of the 'REFERENCE TEXT'.
    
    CRITICAL INSTRUCTIONS FOR ZERO AI DETECTION:
    1. Analyze the 'REFERENCE TEXT' for:
       - Sentence length variance (Burstiness). Humans mix very short sentences with long ones.
       - Slang/Colloquialism (Bahasa Pasar/Rojak if present).
       - Tone (Sarcastic, Serious, Santai?).
    2. Rewrite the 'DRAFT TEXT' using that exact persona.
    3. DO NOT use typical AI transition words like "Tambahan pula", "Di samping itu", "Kesimpulannya". Use natural transitions like "Lagipun", "Sebab tu lah", "So,".
    4. Introduce small imperfections or casual phrasing if the reference has them.
    5. The goal is High Perplexity and High Burstiness.
    
    ---
    REFERENCE TEXT (STYLE SOURCE):
    {reference}
    ---
    DRAFT TEXT (TO REWRITE):
    {draft}
    ---
    """
    
    response = client.chat.completions.create(
        model=model_pilihan,
        messages=[
            {"role": "system", "content": "You are a human writer mimic. You do not sound like an AI."},
            {"role": "user", "content": prompt_rahsia}
        ],
        temperature=0.7 # 0.7 bagus untuk kreativiti terkawal
    )
    return response.choices[0].message.content

# --- ACTION BUTTON ---
st.divider()

if st.button("✨ Tulis Semula (Ikut Style Saya)", type="primary"):
    if ref_text and draft_text:
        client = OpenAI(api_key=api_key)
        
        with st.spinner("Sedang menganalisis gaya otak anda..."):
            try:
                hasil = humanize_text(client, ref_text, draft_text)
                
                st.subheader("📝 Hasil Tulisan (Humanized):")
                st.write(hasil)
                
                st.divider()
                st.code(hasil, language="text") # Senang copy
                st.success("Siap! Cuba check dekat ZeroGPT.")
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Sila isi kedua-dua kotak di atas.")
