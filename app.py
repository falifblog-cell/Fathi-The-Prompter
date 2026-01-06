import streamlit as st
import math

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="Kalkulator Saham Pro", page_icon="📈", layout="centered")

# --- 2. SIDEBAR (TEMA & INFO) ---
with st.sidebar:
    st.header("⚙️ Tetapan")
    tema = st.radio("Pilih Tema:", ["🌙 Mode Gelap (Dark)", "☀️ Mode Cerah (Light)"])
    
    st.divider()
    
    st.header("ℹ️ Intraday vs Normal")
    st.info("""
    **Apa itu Intraday Rate?**
    Rate diskaun jika anda Beli & Jual kaunter sama pada **HARI YANG SAMA**.
    
    **Siapa untung?**
    - Pengguna akaun **Normal / Margin** (Jimat banyak!).
    - Pengguna **Cash Upfront** (MPlus/Rakuten) biasanya tiada beza (Flat Rate).
    """)

# --- 3. CSS (HILANGKAN BRANDING) ---
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
st.caption("Perbandingan Untung: Intraday (Hari Sama) vs Swing (Simpan).")

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

# Senarai Broker dengan Logik Intraday vs Normal
list_broker = [
    "MPlus Cash Upfront (Flat 0.05%)",
    "MPlus Normal/Margin (Intraday 0.05% | Swing 0.42%)",
    "Inv. Bank Normal (Intraday 0.15% | Swing 0.42%)", 
    "Rakuten Trade (Tiered Flat)",
    "HLIB / Promo (Flat 0.08%)",
    "Maybank/CIMB Cash (Flat 0.42%)"
]
pilihan_broker = st.selectbox("Jenis Akaun Broker:", list_broker, index=0)

# --- 5. LOGIK KIRAAN (BACKEND) ---
def kira_fee_mengikut_jenis(nilai_trade, jenis_broker, is_intraday):
    
    brokerage_rate = 0.0
    min_fee = 0.0
    fee_desc = ""

    # --- LOGIK 1: MPlus Cash (Flat) ---
    if "MPlus Cash" in jenis_broker:
        brokerage_rate = 0.0005
        min_fee = 8.00
        fee_desc = "0.05% (Min RM8)"

    # --- LOGIK 2: MPlus Normal (Beza Besar!) ---
    elif "MPlus Normal" in jenis_broker:
        if is_intraday:
            brokerage_rate = 0.0005 # Intraday murah
            min_fee = 8.00
            fee_desc = "Intra: 0.05% (Min RM8)"
        else:
            brokerage_rate = 0.0042 # Swing mahal
            min_fee = 12.00
            fee_desc = "Swing: 0.42% (Min RM12)"

    # --- LOGIK 3: Investment Bank Normal (Maybank/CIMB/RHB Normal) ---
    elif "Inv. Bank Normal" in jenis_broker:
        if is_intraday:
            brokerage_rate = 0.0015 # Intraday 0.15%
            min_fee = 12.00 # Selalunya min RM12
            fee_desc = "Intra: 0.15% (Min RM12)"
        else:
            brokerage_rate = 0.0042 # Standard 0.42%
            min_fee = 12.00
            fee_desc = "Swing: 0.42% (Min RM12)"

    # --- LOGIK 4: Rakuten (Tiered Flat) ---
    elif "Rakuten" in jenis_broker:
        # Rakuten tiada beza intraday/swing, ikut tier
        if nilai_trade <= 1000:
            return 7.00, "Flat RM7"
        elif nilai_trade <= 9999.99:
            return 9.00, "Flat RM9"
        else:
            brokerage_rate = 0.001
            min_fee = 0.0 # Max capping RM100 handled below
            fee_desc = "0.10%"
            
            # Special Cap Rakuten
            base_fee = nilai_trade * brokerage_rate
            return min(base_fee, 100.00), fee_desc

    # --- LOGIK 5: HLIB / Promo (Flat) ---
    elif "HLIB" in jenis_broker:
        brokerage_rate = 0.0008
        min_fee = 8.00
        fee_desc = "0.08% (Min RM8)"

    # --- LOGIK 6: Maybank/CIMB Cash (Flat Mahal) ---
    elif "Maybank/CIMB Cash" in jenis_broker:
        brokerage_rate = 0.0042
        min_fee = 12.00
        fee_desc = "0.42% (Min RM12)"

    # Kira Brokerage
    brokerage_rm = max(nilai_trade * brokerage_rate, min_fee)
    return brokerage_rm, fee_desc

def kira_total_kos(nilai_trade, jenis_broker, is_intraday):
    # 1. Brokerage
    brokerage_rm, desc = kira_fee_mengikut_jenis(nilai_trade, jenis_broker, is_intraday)
    
    # 2. Clearing (0.03%)
    clearing = min(nilai_trade * 0.0003, 1000.00)
    
    # 3. Stamp Duty (RM1.50/1000)
    stamp = min(math.ceil(nilai_trade / 1000) * 1.50, 1000.00)
    
    # 4. SST (0%)
    sst = 0.00
    
    total_fee = brokerage_rm + clearing + stamp + sst
    return total_fee, desc

# PROSES MATEMATIK
unit_total = lot_size * 100
nilai_beli_kasar = buy_price * unit_total
nilai_jual_kasar = sell_price * unit_total

# --- KIRAAN SENARIO A: INTRADAY ---
fee_beli_intra, desc_beli_intra = kira_total_kos(nilai_beli_kasar, pilihan_broker, is_intraday=True)
fee_jual_intra, desc_jual_intra = kira_total_kos(nilai_jual_kasar, pilihan_broker, is_intraday=True)

net_profit_intra = nilai_jual_kasar - fee_jual_intra - (nilai_beli_kasar + fee_beli_intra)
roi_intra = (net_profit_intra / (nilai_beli_kasar + fee_beli_intra)) * 100 if nilai_beli_kasar > 0 else 0

# --- KIRAAN SENARIO B: SWING (NORMAL) ---
fee_beli_norm, desc_beli_norm = kira_total_kos(nilai_beli_kasar, pilihan_broker, is_intraday=False)
fee_jual_norm, desc_jual_norm = kira_total_kos(nilai_jual_kasar, pilihan_broker, is_intraday=False)

net_profit_norm = nilai_jual_kasar - fee_jual_norm - (nilai_beli_kasar + fee_beli_norm)
roi_norm = (net_profit_norm / (nilai_beli_kasar + fee_beli_norm)) * 100 if nilai_beli_kasar > 0 else 0


# --- 6. PAPARAN OUTPUT (SIDE BY SIDE) ---
st.divider()

if st.button("🧮 Bandingkan Untung", type="primary"):
    
    st.subheader("3. Perbandingan Keputusan")
    
    # KITA BUAT 2 KOLUM BESAR
    col_intra, col_norm = st.columns(2)
    
    # --- KOLUM KIRI: INTRADAY ---
    with col_intra:
        st.info("⚡ JUAL HARI SAMA (Intraday)")
        
        # Untung Bersih
        if net_profit_intra > 0:
            st.metric("Untung Bersih", f"RM {net_profit_intra:,.2f}", f"{roi_intra:.2f}%")
        else:
            st.metric("Untung Bersih", f"RM {net_profit_intra:,.2f}", f"{roi_intra:.2f}%", delta_color="inverse")
            
        st.write(f"**Rate Beli:** {desc_beli_intra}")
        st.write(f"**Rate Jual:** {desc_jual_intra}")
        st.write(f"Total Kos: RM {(fee_beli_intra + fee_jual_intra):.2f}")

    # --- KOLUM KANAN: SWING ---
    with col_norm:
        st.success("📅 JUAL ESOK / LUSA (Swing)")
        
        # Untung Bersih
        if net_profit_norm > 0:
            st.metric("Untung Bersih", f"RM {net_profit_norm:,.2f}", f"{roi_norm:.2f}%")
        else:
            st.metric("Untung Bersih", f"RM {net_profit_norm:,.2f}", f"{roi_norm:.2f}%", delta_color="inverse")
            
        st.write(f"**Rate Beli:** {desc_beli_norm}")
        st.write(f"**Rate Jual:** {desc_jual_norm}")
        st.write(f"Total Kos: RM {(fee_beli_norm + fee_jual_norm):.2f}")

    st.divider()
    
    # ANALISIS
    diff = net_profit_intra - net_profit_norm
    if diff > 0.05: # Kalau ada beza lebih 5 sen
        st.warning(f"💡 **JIMAT:** Kalau jual hari ni (Intraday), tuan untung extra **RM {diff:.2f}** sebab fee lebih murah!")
    elif diff == 0:
        st.caption("ℹ️ Tiada beza kos antara Intraday atau Swing untuk broker ini.")
    
    # DETAIL TABLE
    with st.expander("Lihat Perincian Modal & Kos"):
        st.write("#### Fasa Beli (Modal Keluar)")
        d1, d2 = st.columns(2)
        d1.write(f"**Intraday:** RM {(nilai_beli_kasar + fee_beli_intra):.2f}")
        d2.write(f"**Swing:** RM {(nilai_beli_kasar + fee_beli_norm):.2f}")
        
        st.write("#### Fasa Jual (Duit Masuk)")
        d3, d4 = st.columns(2)
        d3.write(f"**Intraday:** RM {(nilai_jual_kasar - fee_jual_intra):.2f}")
        d4.write(f"**Swing:** RM {(nilai_jual_kasar - fee_jual_norm):.2f}")
