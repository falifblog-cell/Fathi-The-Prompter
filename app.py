import streamlit as st
import math

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="Kalkulator Saham Pro", page_icon="📈", layout="centered")

# --- 2. SIDEBAR (TEMA & INFO) ---
with st.sidebar:
    st.header("⚙️ Tetapan")
    tema = st.radio("Pilih Tema:", ["🌙 Mode Gelap (Dark)", "☀️ Mode Cerah (Light)"])
    
    st.divider()
    
    st.header("ℹ️ Info Rate MPlus Global")
    st.info("""
    **Struktur Fee Rasmi (Bursa):**
    
    1. **Intraday (Jual Hari Sama)**
    - Rate: **0.05%** (Min RM8).
    
    2. **Swing (Jual Hari Lain)**
    - Bawah RM50k: **0.08%**
    - Atas RM50k: **0.05%**
    
    *Ini adalah kadar rasmi untuk pengguna app MPlus Global & akaun Online.*
    """)
    st.caption("Sumber: mplusonline.com/pricing")

# --- 3. CSS ---
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .viewerBadge_container__1QSob {display: none !important;}
    .styles_viewerBadge__1yB5_ {display: none !important;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

if tema == "☀️ Mode Cerah (Light)":
    st.markdown("""
        <style>
            .stApp { background-color: #ffffff; color: #000000; }
            .stNumberInput input { color: #000000 !important; background-color: #f0f2f6 !important; }
            .stMarkdown, .stText, p, label, .stMetricLabel { color: #000000 !important; }
            div[data-testid="stMetricValue"] { color: #000000 !important; }
        </style>
    """, unsafe_allow_html=True)

# --- 4. TITLE & INPUT ---
st.title("📈 Kalkulator Saham Pro")
st.caption("Kira untung bersih: Intraday (0.05%) vs Swing (0.08%).")

st.subheader("1. Masukkan Detail Trade")
col1, col2 = st.columns(2)

# INPUT BELI
with col1:
    st.info("🟢 BUY (Beli)")
    buy_price = st.number_input("Harga Beli (RM)", value=0.500, step=0.005, format="%.3f")
    lot_size = st.number_input("Berapa Lot?", value=1, step=1, help="1 Lot = 100 Unit")
    raw_beli = buy_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :green[RM {raw_beli:,.2f}]")

# INPUT JUAL
with col2:
    st.error("🔴 SELL (Jual)")
    sell_price = st.number_input("Harga Jual (RM)", value=0.550, step=0.005, format="%.3f")
    st.write(f"Jual: {lot_size} Lot") 
    raw_jual = sell_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :red[RM {raw_jual:,.2f}]")

# PILIH BROKER
st.divider()
st.subheader("2. Pilih Broker")

list_broker = [
    "MPlus Global / Online (Tiered Rate)",
    "MPlus Cash Upfront (Legacy Flat 0.05%)",
    "CGS-CIMB iCash (Flat 0.06%)",
    "MPlus Normal (Margin/Limit)",
    "Rakuten Trade (Tiered Flat)",
    "Custom Rate (Set Sendiri)"
]
pilihan_broker = st.selectbox("Jenis Akaun Broker:", list_broker, index=0)

# --- 5. LOGIK KIRAAN (BACKEND) ---
def kira_total_kos(nilai_trade, jenis_broker, is_intraday, input_custom=None):
    
    brokerage_rm = 0.0
    desc = ""
    min_fee = 0.0
    rate_used = 0.0

    # --- LOGIK 1: MPlus Global / Online (Tiered) ---
    if "MPlus Global" in jenis_broker:
        min_fee = 8.00
        
        if is_intraday:
            # Intraday rate
            rate_used = 0.05
        else:
            # Swing rate bergantung Tier RM50k
            if nilai_trade > 50000:
                rate_used = 0.05
            else:
                rate_used = 0.08
        
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = f"{rate_used}% (Min RM8)"

    # --- LOGIK 2: MPlus Cash Upfront (Legacy) ---
    elif "MPlus Cash Upfront" in jenis_broker:
        min_fee = 8.00
        rate_used = 0.05
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = "0.05% (Min RM8)"

    # --- LOGIK 3: CGS-CIMB iCash ---
    elif "CGS-CIMB" in jenis_broker:
        min_fee = 8.00
        rate_used = 0.06
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = "0.06% (Min RM8)"

    # --- LOGIK 4: MPlus Normal (Margin) ---
    elif "MPlus Normal" in jenis_broker:
        if is_intraday:
            rate_used = 0.05
            min_fee = 8.00
            desc = "0.05% (Min RM8)"
        else:
            rate_used = 0.42
            min_fee = 12.00
            desc = "0.42% (Min RM12)"
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)

    # --- LOGIK 5: Rakuten ---
    elif "Rakuten" in jenis_broker:
        if nilai_trade <= 1000: return 7.00 + min(nilai_trade * 0.0003, 1000) + min(math.ceil(nilai_trade/1000)*1.5, 1000), "Flat RM7"
        elif nilai_trade <= 9999.99: return 9.00 + min(nilai_trade * 0.0003, 1000) + min(math.ceil(nilai_trade/1000)*1.5, 1000), "Flat RM9"
        else:
            brokerage_rm = min(nilai_trade * 0.001, 100.00)
            desc = "0.10%"

    # --- LOGIK 6: Custom ---
    elif "Custom" in jenis_broker and input_custom:
        r_intra, r_swing, r_min = input_custom
        rate_used = r_intra if is_intraday else r_swing
        min_fee = r_min
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = f"{rate_used:.2f}% (Min RM{min_fee:.0f})"

    # Fallback
    if brokerage_rm == 0 and "Rakuten" not in jenis_broker:
        brokerage_rm = max(nilai_trade * 0.0005, 8.00)

    # Caj Wajib Lain
    clearing = min(nilai_trade * 0.0003, 1000.00)
    stamp = min(math.ceil(nilai_trade / 1000) * 1.50, 1000.00)
    sst = 0.00 # SST 0%
    
    total_fee = brokerage_rm + clearing + stamp + sst
    return total_fee, desc

# PROSES MATEMATIK
unit_total = lot_size * 100
nilai_beli_kasar = buy_price * unit_total
nilai_jual_kasar = sell_price * unit_total

# CUSTOM INPUT
custom_vals = None
if "Custom" in pilihan_broker:
    st.info("🛠️ Masukkan rate broker anda (dalam %)")
    c1, c2, c3 = st.columns(3)
    r_i = c1.number_input("Rate Intraday (%)", value=0.05, step=0.01)
    r_s = c2.number_input("Rate Swing (%)", value=0.08, step=0.01)
    r_m = c3.number_input("Min Fee (RM)", value=8.00, step=1.00)
    custom_vals = (r_i, r_s, r_m)

# KIRAAN
fee_beli_intra, desc_beli_intra = kira_total_kos(nilai_beli_kasar, pilihan_broker, True, custom_vals)
fee_jual_intra, desc_jual_intra = kira_total_kos(nilai_jual_kasar, pilihan_broker, True, custom_vals)
net_intra = nilai_jual_kasar - fee_jual_intra - (nilai_beli_kasar + fee_beli_intra)
roi_intra = (net_intra / (nilai_beli_kasar + fee_beli_intra)) * 100 if nilai_beli_kasar > 0 else 0

fee_beli_norm, desc_beli_norm = kira_total_kos(nilai_beli_kasar, pilihan_broker, False, custom_vals)
fee_jual_norm, desc_jual_norm = kira_total_kos(nilai_jual_kasar, pilihan_broker, False, custom_vals)
net_norm = nilai_jual_kasar - fee_jual_norm - (nilai_beli_kasar + fee_beli_norm)
roi_norm = (net_norm / (nilai_beli_kasar + fee_beli_norm)) * 100 if nilai_beli_kasar > 0 else 0


# --- 6. PAPARAN OUTPUT ---
st.divider()

if st.button("🧮 Bandingkan Untung", type="primary"):
    
    st.subheader("3. Perbandingan Keputusan")
    
    col_intra, col_norm = st.columns(2)
    
    # INTRADAY
    with col_intra:
        st.info("⚡ JUAL HARI SAMA (Intraday)")
        if net_intra > 0: st.metric("Untung Bersih", f"RM {net_intra:,.2f}", f"{roi_intra:.2f}%")
        else: st.metric("Untung Bersih", f"RM {net_intra:,.2f}", f"{roi_intra:.2f}%", delta_color="inverse")
        st.caption(f"Rate: {desc_beli_intra}")
        st.write(f"Total Kos: RM {(fee_beli_intra + fee_jual_intra):.2f}")

    # SWING
    with col_norm:
        st.success("📅 JUAL ESOK (Swing)")
        if net_norm > 0: st.metric("Untung Bersih", f"RM {net_norm:,.2f}", f"{roi_norm:.2f}%")
        else: st.metric("Untung Bersih", f"RM {net_norm:,.2f}", f"{roi_norm:.2f}%", delta_color="inverse")
        st.caption(f"Rate: {desc_beli_norm}")
        st.write(f"Total Kos: RM {(fee_beli_norm + fee_jual_norm):.2f}")

    st.divider()
    
    # Logic Jimat / Beza
    diff = net_intra - net_norm
    if diff > 0.05:
        st.warning(f"💡 **BEZA:** Untung Intraday lebih tinggi sebab fee 0.05%. Swing fee 0.08% (jika < RM50k).")
    elif diff == 0:
        st.info("ℹ️ **TIADA BEZA:** Rate sama (Trade > RM50k atau kena Min Fee RM8).")
    
    with st.expander("Lihat Perincian Modal"):
        st.write(f"**Modal Intraday:** RM {(nilai_beli_kasar + fee_beli_intra):.2f}")
        st.write(f"**Modal Swing:** RM {(nilai_beli_kasar + fee_beli_norm):.2f}")
