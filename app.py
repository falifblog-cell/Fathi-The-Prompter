import streamlit as st
import math

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="Kalkulator Saham Pro", page_icon="📈", layout="centered")

# --- 2. SIDEBAR (TEMA & INFO) ---
with st.sidebar:
    st.header("⚙️ Tetapan")
    tema = st.radio("Pilih Tema:", ["🌙 Mode Gelap (Dark)", "☀️ Mode Cerah (Light)"])
    
    st.divider()
    
    st.header("ℹ️ Info Fee Broker")
    st.info("""
    **Nota Fee Minimum:**
    Walaupun % fee rendah, broker akan caj ikut **MINIMUM** jika nilai trade kecil.
    
    Contoh: Beli saham RM50.
    Fee 0.05% = 2 sen.
    Tapi Broker Minimum = **RM8.00**.
    Maka tuan kena bayar RM8.00.
    """)
    st.caption("Nota: MPlus Global Apps ikut rate MPlus Online (0.05% Min RM8) untuk Saham Bursa.")

# --- 3. CSS (HILANGKAN BRANDING & TEMA) ---
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
st.caption("Kira untung bersih & kos sebenar trade Bursa Malaysia.")

st.subheader("1. Masukkan Detail Trade")
col1, col2 = st.columns(2)

# INPUT BELI
with col1:
    st.info("🟢 BUY (Beli)")
    buy_price = st.number_input("Harga Beli (RM)", value=0.500, step=0.005, format="%.3f")
    lot_size = st.number_input("Berapa Lot?", value=1, step=1, help="1 Lot = 100 Unit")
    
    # Kiraan 'Live' kat bawah input
    raw_beli = buy_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :green[RM {raw_beli:,.2f}]")

# INPUT JUAL
with col2:
    st.error("🔴 SELL (Jual)")
    sell_price = st.number_input("Harga Jual (RM)", value=0.550, step=0.005, format="%.3f")
    st.write(f"Jual: {lot_size} Lot") 
    
    # Kiraan 'Live' kat bawah input
    raw_jual = sell_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :red[RM {raw_jual:,.2f}]")

# PILIH BROKER
st.divider()
st.subheader("2. Pilih Broker")

list_broker = [
    "MPlus / MPlus Global (Cash Upfront) - 0.05% | Min RM8",
    "MPlus (Normal / Margin) - 0.42% | Min RM12",
    "Rakuten Trade (Tier 1: < RM1k) - Flat RM7",
    "Rakuten Trade (Tier 2: RM1k - RM10k) - Flat RM9",
    "Rakuten Trade (Tier 3: > RM10k) - 0.10% | Max RM100",
    "Maybank / CGS / RHB / Public (Cash Upfront) - 0.42% | Min RM12",
    "Investment Bank (Normal / Remisier) - 0.60% | Min RM40",
    "Custom Rate (0.10%) - CGS Promo / Lain-lain",
    "Tiada Kos (Paper Trade)"
]
pilihan_broker = st.selectbox("Jenis Akaun Broker:", list_broker, index=0)

# --- 5. LOGIK KIRAAN (BACKEND) ---
def kira_kos_broker_malaysia(nilai_trade, jenis_broker):
    if "Tiada Kos" in jenis_broker:
        return 0.0, 0.0
    
    brokerage_fee = 0.0
    
    # Logic Rakuten
    if "Rakuten" in jenis_broker:
        if nilai_trade <= 1000: brokerage_fee = 7.00
        elif nilai_trade <= 9999.99: brokerage_fee = 9.00
        else: brokerage_fee = min(nilai_trade * 0.001, 100.00)
    # Logic MPlus Cash
    elif "MPlus / MPlus Global (Cash Upfront)" in jenis_broker:
        brokerage_fee = max(nilai_trade * 0.0005, 8.00)
    # Logic MPlus Normal
    elif "MPlus (Normal" in jenis_broker:
        brokerage_fee = max(nilai_trade * 0.0042, 12.00)
    # Logic Bank Cash
    elif "Cash Upfront)" in jenis_broker:
        brokerage_fee = max(nilai_trade * 0.0042, 12.00)
    # Logic Remisier
    elif "Remisier" in jenis_broker:
        brokerage_fee = max(nilai_trade * 0.0060, 40.00)
    # Logic Custom
    elif "Custom" in jenis_broker:
        brokerage_fee = max(nilai_trade * 0.0010, 8.00)

    # Caj Wajib Lain
    clearing_fee = min(nilai_trade * 0.0003, 1000.00)
    stamp_duty = min(math.ceil(nilai_trade / 1000) * 1.50, 1000.00)
    sst = brokerage_fee * 0.08
    
    total_fee = brokerage_fee + clearing_fee + stamp_duty + sst
    return total_fee, brokerage_fee

# PROSES MATEMATIK
unit_total = lot_size * 100

# 1. Kira Nilai Kasar (Ini Slot yang Tuan Nak)
nilai_beli_kasar = buy_price * unit_total
nilai_jual_kasar = sell_price * unit_total

# 2. Kira Fee
kos_beli, broker_beli = kira_kos_broker_malaysia(nilai_beli_kasar, pilihan_broker)
kos_jual, broker_jual = kira_kos_broker_malaysia(nilai_jual_kasar, pilihan_broker)

# 3. Kira Total Akhir
total_modal_keluar = nilai_beli_kasar + kos_beli
total_bersih_dapat = nilai_jual_kasar - kos_jual

# 4. Untung Bersih
untung_bersih = total_bersih_dapat - total_modal_keluar
peratus_untung = (untung_bersih / total_modal_keluar) * 100 if total_modal_keluar > 0 else 0
total_fee_hangus = kos_beli + kos_jual

# --- 6. PAPARAN OUTPUT (YANG BARU) ---
st.divider()

if st.button("🧮 Kira Untung Bersih", type="primary"):
    
    st.subheader("3. Analisis Kewangan")

    # --- ROW 1: FASA BELI (INI YANG TUAN MINTA) ---
    st.markdown("#### 🟢 Fasa Beli (Modal)")
    b1, b2, b3 = st.columns(3)
    
    # SLOT 1: NILAI SAHAM (Harga x Lot)
    b1.metric("1. Nilai Saham (Ikut Lot)", f"RM {nilai_beli_kasar:,.2f}", help="Harga Beli x Unit Saham")
    
    # SLOT 2: FEE TAMBAHAN
    b2.metric("2. Caj Broker & Tax", f"RM {kos_beli:,.2f}", help="Duit hangus untuk fee")
    
    # SLOT 3: TOTAL KELUAR BANK
    b3.metric("3. Total Modal Kena Ada", f"RM {total_modal_keluar:,.2f}", delta="- Tolak Bank", delta_color="inverse")
    
    st.markdown("---")

    # --- ROW 2: FASA JUAL (PULANGAN) ---
    st.markdown("#### 🔴 Fasa Jual (Pulangan)")
    j1, j2, j3 = st.columns(3)
    
    j1.metric("1. Nilai Jual (Ikut Lot)", f"RM {nilai_jual_kasar:,.2f}")
    j2.metric("2. Caj Broker & Tax", f"RM {kos_jual:,.2f}")
    j3.metric("3. Duit Masuk Bank", f"RM {total_bersih_dapat:,.2f}", delta="+ Masuk Bank")
    
    st.divider()
    
    # --- ROW 3: KEPUTUSAN ---
    if untung_bersih > 0:
        st.success(f"### 🎉 UNTUNG BERSIH: RM {untung_bersih:,.2f}")
        st.write(f"ROI: **+{peratus_untung:.2f}%**")
        st.balloons()
    elif untung_bersih < 0:
        st.error(f"### 💸 RUGI BERSIH: RM {untung_bersih:,.2f}")
        st.write(f"ROI: **{peratus_untung:.2f}%**")
    else:
        st.warning("### 😐 BALIK MODAL (Breakeven)")

    # Detail Fee
    with st.expander("Lihat Perincian Fee"):
        st.write(f"**Total Fee Hangus (Beli + Jual):** RM {total_fee_hangus:.2f}")
