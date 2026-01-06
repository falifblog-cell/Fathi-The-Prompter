import streamlit as st
import math

# --- SETUP MUKA SURAT ---
st.set_page_config(page_title="Kalkulator Saham Pro", page_icon="📈", layout="centered")

# --- FUNGSI TUKAR TEMA & NOTA TEPI (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Tetapan")
    tema = st.radio("Pilih Tema:", ["🌙 Mode Gelap (Dark)", "☀️ Mode Cerah (Light)"])
    
    st.divider()
    
    # --- NOTA PASAL FEE ---
    st.header("ℹ️ Info Fee Broker")
    st.info("""
    **Kenapa Kena RM8?**
    Broker akan caj ikut mana yang **LEBIH TINGGI** antara "%" atau "Minimum".
    
    **Contoh: MPlus (Min RM8)**
    - Jika trade kecil (bawah RM16k), fee % mungkin cuma RM2. Tapi broker tetap caj **RM8**.
    - Jika trade besar (atas RM16k), baru broker caj ikut **0.05%**.
    """)
    
    st.caption("Nota MPlus Global: Jika trade Saham Bursa guna apps Global, fee dia sama macam MPlus Online (0.05% Min RM8).")

# Logic CSS (Tema)
if tema == "☀️ Mode Cerah (Light)":
    st.markdown("""
        <style>
            .stApp { background-color: #ffffff; color: #000000; }
            .stNumberInput input { color: #000000 !important; background-color: #f0f2f6 !important; }
            .stMarkdown, .stText, p, label, .stMetricLabel { color: #000000 !important; }
            div[data-testid="stMetricValue"] { color: #000000 !important; }
        </style>
    """, unsafe_allow_html=True)

# --- JUDUL APP (YANG DITUKAR) ---
st.title("📈 Kalkulator Saham Pro")
st.caption("Kira untung bersih sebenar mengikut struktur fee terkini Broker Malaysia.")

# --- BAHAGIAN 1: INPUT DATA ---
st.subheader("1. Masukkan Detail Trade")

col1, col2 = st.columns(2)

# KOLUM BELI
with col1:
    st.info("🟢 BUY (Beli)")
    buy_price = st.number_input("Harga Beli (RM)", value=0.500, step=0.005, format="%.3f")
    lot_size = st.number_input("Berapa Lot?", value=1, step=1, help="1 Lot = 100 Unit")
    
    total_beli_raw = buy_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :green[RM {total_beli_raw:,.2f}]")

# KOLUM JUAL
with col2:
    st.error("🔴 SELL (Jual)")
    sell_price = st.number_input("Harga Jual (RM)", value=0.550, step=0.005, format="%.3f")
    st.write(f"Jual: {lot_size} Lot") 
    
    total_jual_raw = sell_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :red[RM {total_jual_raw:,.2f}]")

# --- PILIHAN BROKER MALAYSIA LENGKAP ---
st.divider()
st.subheader("2. Pilih Broker")

# Senarai Broker
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

# --- FUNGSI LOGIK KIRAAN KOS SEBENAR ---
def kira_kos_broker_malaysia(nilai_trade, jenis_broker):
    if "Tiada Kos" in jenis_broker:
        return 0.0, 0.0
    
    brokerage_fee = 0.0
    
    # --- LOGIK 1: RAKUTEN TRADE (TIER SYSTEM) ---
    if "Rakuten" in jenis_broker:
        if nilai_trade <= 1000:
            brokerage_fee = 7.00
        elif nilai_trade <= 9999.99:
            brokerage_fee = 9.00
        else:
            fee_calc = nilai_trade * 0.001
            brokerage_fee = min(fee_calc, 100.00)
            
    # --- LOGIK 2: MPLUS CASH / GLOBAL (BURSA) ---
    elif "MPlus / MPlus Global (Cash Upfront)" in jenis_broker:
        fee_calc = nilai_trade * 0.0005
        brokerage_fee = max(fee_calc, 8.00)

    # --- LOGIK 3: MPLUS NORMAL ---
    elif "MPlus (Normal" in jenis_broker:
        fee_calc = nilai_trade * 0.0042
        brokerage_fee = max(fee_calc, 12.00)

    # --- LOGIK 4: BANK CASH UPFRONT (General) ---
    elif "Cash Upfront)" in jenis_broker:
        fee_calc = nilai_trade * 0.0042
        brokerage_fee = max(fee_calc, 12.00)
        
    # --- LOGIK 5: NORMAL / REMISIER ---
    elif "Remisier" in jenis_broker:
        fee_calc = nilai_trade * 0.0060
        brokerage_fee = max(fee_calc, 40.00)
        
    # --- LOGIK 6: CUSTOM / PROMO ---
    elif "Custom" in jenis_broker:
        fee_calc = nilai_trade * 0.0010
        brokerage_fee = max(fee_calc, 8.00)

    # --- CAJ WAJIB LAIN (BURSA MALAYSIA & KERAJAAN) ---
    clearing_fee = min(nilai_trade * 0.0003, 1000.00)
    stamp_duty = math.ceil(nilai_trade / 1000) * 1.50
    stamp_duty = min(stamp_duty, 1000.00)
    sst = brokerage_fee * 0.08
    
    total_kos = brokerage_fee + clearing_fee + stamp_duty + sst
    
    return total_kos, brokerage_fee

# --- PENGIRAAN ---
unit_total = lot_size * 100
nilai_beli_kasar = buy_price * unit_total
nilai_jual_kasar = sell_price * unit_total

kos_beli, broker_beli = kira_kos_broker_malaysia(nilai_beli_kasar, pilihan_broker)
kos_jual, broker_jual = kira_kos_broker_malaysia(nilai_jual_kasar, pilihan_broker)
total_fee_hangus = kos_beli + kos_jual

total_duit_keluar = nilai_beli_kasar + kos_beli
total_duit_masuk = nilai_jual_kasar - kos_jual
untung_bersih = total_duit_masuk - total_duit_keluar
peratus_untung = (untung_bersih / total_duit_keluar) * 100 if total_duit_keluar > 0 else 0

# --- PAPARAN KEPUTUSAN ---
st.divider()

if st.button("🧮 Kira Untung Bersih", type="primary"):
    
    st.subheader("3. Keputusan Kewangan")
    
    k1, k2 = st.columns(2)
    k1.metric("💸 Modal Kena Ada (Total)", f"RM {total_duit_keluar:,.2f}", delta="- Termasuk Fee", delta_color="inverse")
    k2.metric("💰 Duit Masuk Bersih", f"RM {total_duit_masuk:,.2f}", delta="+ Lepas Tolak Fee")
    
    st.divider()
    
    if untung_bersih > 0:
        st.success(f"### 🎉 UNTUNG BERSIH: RM {untung_bersih:,.2f}")
        st.write(f"ROI: **+{peratus_untung:.2f}%**")
        st.balloons()
    elif untung_bersih < 0:
        st.error(f"### 💸 RUGI BERSIH: RM {untung_bersih:,.2f}")
        st.write(f"ROI: **{peratus_untung:.2f}%**")
    else:
        st.warning("### 😐 BALIK MODAL (Breakeven)")

    with st.expander("🔍 Tengok Perincian Fee (Broker + Bursa + Gov)"):
        st.write("### Semasa Beli")
        st.text(f"Harga Saham : RM {nilai_beli_kasar:,.2f}")
        st.text(f"Brokerage   : RM {broker_beli:.2f} (Base Fee)")
        st.text(f"Total Caj   : RM {kos_beli:.2f} (Termasuk SST, Stamp, Clearing)")
        
        st.write("### Semasa Jual")
        st.text(f"Harga Saham : RM {nilai_jual_kasar:,.2f}")
        st.text(f"Brokerage   : RM {broker_jual:.2f} (Base Fee)")
        st.text(f"Total Caj   : RM {kos_jual:.2f} (Termasuk SST, Stamp, Clearing)")
        
        st.markdown(f"**TOTAL FEE HANGUS (Beli + Jual): RM {total_fee_hangus:.2f}**")
        st.caption("*Nota: Kiraan SST adalah 8% (Kadar baharu 2024). Stamp Duty RM1.50/RM1000.*")
