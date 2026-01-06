import streamlit as st
import math

# --- SETUP ---
st.set_page_config(page_title="Kalkulator Saham Fathi", page_icon="📈", layout="centered")

st.title("📈 Kalkulator Untung Saham")
st.caption("Kira untung bersih (Net Profit) selepas tolak kos broker Bursa Malaysia.")

# --- INPUT DATA ---
st.markdown("### 1. Masukkan Detail Trade")

col1, col2 = st.columns(2)

with col1:
    st.info("🟢 BUY (Beli)")
    buy_price = st.number_input("Harga Beli Satu Unit (RM)", value=0.500, step=0.005, format="%.3f")
    lot_size = st.number_input("Berapa Lot?", value=1, step=1, help="1 Lot = 100 Unit")
    
with col2:
    st.error("🔴 SELL (Jual)")
    sell_price = st.number_input("Harga Jual Satu Unit (RM)", value=0.550, step=0.005, format="%.3f")
    
    # Pilihan Broker
    broker_type = st.selectbox("Jenis Broker:", 
                               ["Cash Upfront (Murah - 0.05%)", "Normal (0.42%)", "Min RM 8 (Standard)", "Tiada Kos (Paper Trade)"])

# --- FUNGSI KIRA KOS BURSA ---
def kira_kos(nilai_trade, jenis_broker):
    if jenis_broker == "Tiada Kos (Paper Trade)":
        return 0.0
    
    # 1. Brokerage Fee
    rate = 0.0
    min_fee = 0.0
    
    if "0.05%" in jenis_broker: rate = 0.0005 # Rakuten/Mplus Cash
    elif "0.42%" in jenis_broker: rate = 0.0042 # Maybank/CIMB Normal
    elif "Min RM 8" in jenis_broker: 
        rate = 0.0042 
        min_fee = 8.00
        
    brokerage = max(nilai_trade * rate, min_fee)
    
    # 2. Clearing Fee (0.03% max RM1000)
    clearing = min(nilai_trade * 0.0003, 1000.0)
    
    # 3. Stamp Duty (RM1.50 per RM1000, max RM1000)
    # Formula: Round up setiap 1000
    stamp = math.ceil(nilai_trade / 1000) * 1.50
    stamp = min(stamp, 1000.0)
    
    # 4. SST (8% atas Brokerage sahaja)
    sst = brokerage * 0.08
    
    total_kos = brokerage + clearing + stamp + sst
    return total_kos

# --- LOGIC KIRAAN ---
unit_total = lot_size * 100
nilai_beli_kasar = buy_price * unit_total
nilai_jual_kasar = sell_price * unit_total

kos_beli = kira_kos(nilai_beli_kasar, broker_type)
kos_jual = kira_kos(nilai_jual_kasar, broker_type)
total_kos_transaksi = kos_beli + kos_jual

# Untung Kasar vs Bersih
untung_kasar = nilai_jual_kasar - nilai_beli_kasar
untung_bersih = untung_kasar - total_kos_transaksi
peratus_untung = (untung_bersih / nilai_beli_kasar) * 100 if nilai_beli_kasar > 0 else 0

# --- PAPARAN HASIL ---
st.divider()
st.markdown("### 2. Keputusan")

if st.button("🧮 Kira Sekarang", type="primary"):
    
    # Tunjuk Kad Keputusan
    c1, c2, c3 = st.columns(3)
    c1.metric("Modal Kasar", f"RM {nilai_beli_kasar:,.2f}")
    c2.metric("Nilai Jual", f"RM {nilai_jual_kasar:,.2f}")
    c3.metric("Kos Hangus (Fee)", f"RM {total_kos_transaksi:,.2f}", help="Brokerage + SST + Clearing + Stamp")
    
    st.divider()
    
    # Tunjuk Profit Besar-Besar
    if untung_bersih > 0:
        st.success(f"### 🎉 UNTUNG BERSIH: RM {untung_bersih:,.2f}")
        st.write(f"ROI: **+{peratus_untung:.2f}%**")
        st.balloons()
    elif untung_bersih < 0:
        st.error(f"### 💸 RUGI BERSIH: RM {untung_bersih:,.2f}")
        st.write(f"ROI: **{peratus_untung:.2f}%**")
    else:
        st.warning("### 😐 BALIK MODAL (Breakeven)")

    # Breakdown Kos (Optional)
    with st.expander("Tengok Perincian Kos"):
        st.write(f"Kos Beli: RM {kos_beli:.2f}")
        st.write(f"Kos Jual: RM {kos_jual:.2f}")
        st.caption("*Kiraan ini adalah anggaran standard Bursa Malaysia.")

else:
    st.info("Tekan butang 'Kira Sekarang' di atas.")
