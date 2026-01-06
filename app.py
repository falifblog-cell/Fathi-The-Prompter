import streamlit as st
import math

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="Kalkulator Saham Pro", page_icon="📈", layout="centered")

# --- 2. SIDEBAR (SENARAI RATE RASMI) ---
with st.sidebar:
    st.header("⚙️ Tetapan")
    tema = st.radio("Pilih Tema:", ["🌙 Mode Gelap (Dark)", "☀️ Mode Cerah (Light)"])
    
    st.divider()
    
    # --- INFO RATE DI TEPI ---
    st.header("📋 Rujukan Rate (2025)")
    st.caption("Semakan di laman web rasmi broker.")
    
    with st.expander("1. MPlus Online / Global", expanded=True):
        st.markdown("""
        * **Intraday:** 0.05% (Min RM8)
        * **Swing (< RM50k):** 0.08% (Min RM8)
        * **Swing (> RM50k):** 0.05% (Min RM8)
        """)
        
    with st.expander("2. Rakuten Trade (Baru)"):
        st.markdown("""
        * **< RM100:** RM1.00 Flat
        * **RM100 - RM9,999:** RM2.88 Flat
        * **RM10k - RM100k:** 0.10%
        * **> RM100k:** RM100.00 Flat
        """)
        
    with st.expander("3. Cash Upfront (Bank)"):
        st.markdown("""
        * **CGS iTrade:** 0.06% (Min RM8)
        * **Maybank Cash:** 0.10% (Min RM8)
        * **HLIB HLeBroking:** ~0.08% (Min RM8)
        """)

    with st.expander("4. Normal / Margin"):
        st.markdown("""
        * **Maybank/CIMB/RHB:** 0.42% (Min RM12/RM28)
        * **Investment Bank Lain:** ~0.60% (Min RM40)
        """)

# --- 3. CSS (STYLE) ---
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
st.caption("Kira untung bersih dengan Rate Rasmi 2025 (MPlus, Rakuten, Maybank, CGS).")

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

# --- SENARAI BROKER (MPlus Online diletakkan paling atas sebagai Default) ---
list_broker = [
    "MPlus Online / Global (Cash Account)", 
    "Rakuten Trade (Rate Baru 2025)",
    "Maybank Investment (Cash Account 0.10%)",
    "CGS iTrade (Cash Account 0.06%)",
    "MPlus Normal / Margin (0.42%)",
    "Investment Bank Normal (0.42% - 0.60%)",
    "Custom Rate (Set Sendiri)"
]

# index=0 bermaksud dia akan pilih yang pertama dalam senarai (MPlus)
pilihan_broker = st.selectbox("Jenis Akaun Broker:", list_broker, index=0)

# --- 5. LOGIK KIRAAN (BACKEND) ---
def kira_total_kos(nilai_trade, jenis_broker, is_intraday, input_custom=None):
    
    brokerage_rm = 0.0
    desc = ""
    min_fee = 0.0
    rate_used = 0.0

    # --- A. MPLUS ONLINE / GLOBAL ---
    if "MPlus Online" in jenis_broker:
        min_fee = 8.00
        if is_intraday:
            rate_used = 0.05
        else:
            # Swing Rate: 0.05% jika > RM50k, 0.08% jika < RM50k
            rate_used = 0.05 if nilai_trade > 50000 else 0.08
        
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = f"{rate_used}% (Min RM8)"

    # --- B. RAKUTEN TRADE (STRUKTUR BARU) ---
    elif "Rakuten" in jenis_broker:
        if nilai_trade <= 100.00:
            brokerage_rm = 1.00
            desc = "Flat RM1"
        elif nilai_trade <= 9999.99:
            brokerage_rm = 2.88
            desc = "Flat RM2.88"
        elif nilai_trade <= 99999.99:
            brokerage_rm = nilai_trade * 0.001
            desc = "0.10%"
        else:
            brokerage_rm = 100.00
            desc = "Flat RM100"

    # --- C. MAYBANK CASH (0.10%) ---
    elif "Maybank Investment" in jenis_broker:
        min_fee = 8.00
        rate_used = 0.10
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = "0.10% (Min RM8)"

    # --- D. CGS iTRADE CASH (0.06%) ---
    elif "CGS iTrade" in jenis_broker:
        min_fee = 8.00
        rate_used = 0.06
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = "0.06% (Min RM8)"

    # --- E. NORMAL ACCOUNT (MARGIN) ---
    elif "Normal" in jenis_broker:
        if is_intraday:
            rate_used = 0.15 # Anggaran Intraday
            min_fee = 12.00
            desc = "Intra: 0.15%"
        else:
            rate_used = 0.42
            min_fee = 12.00
            desc = "Swing: 0.42%"
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)

    # --- F. CUSTOM ---
    elif "Custom" in jenis_broker and input_custom:
        r_intra, r_swing, r_min = input_custom
        rate_used = r_intra if is_intraday else r_swing
        min_fee = r_min
        brokerage_rm = max(nilai_trade * (rate_used / 100), min_fee)
        desc = f"{rate_used:.2f}% (Min RM{min_fee:.0f})"

    # Fallback
    if brokerage_rm == 0 and "Rakuten" not in jenis_broker:
        brokerage_rm = max(nilai_trade * 0.0042, 12.00)

    # Caj Wajib
    clearing = min(nilai_trade * 0.0003, 1000.00)
    stamp = min(math.ceil(nilai_trade / 1000) * 1.50, 1000.00)
    sst = 0.00 # SST 0% untuk Saham Bursa
    
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
        st.warning(f"💡 **BEZA:** Untung Intraday lebih tinggi.")
    elif diff == 0:
        st.info("ℹ️ **TIADA BEZA:** Rate sama untuk trade ini.")
    
    with st.expander("Lihat Perincian Modal"):
        st.write(f"**Modal Intraday:** RM {(nilai_beli_kasar + fee_beli_intra):.2f}")
        st.write(f"**Modal Swing:** RM {(nilai_beli_kasar + fee_beli_norm):.2f}")
