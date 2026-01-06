import streamlit as st
import math

# --- SETUP ---
st.set_page_config(page_title="Kalkulator Saham Fathi", page_icon="📈", layout="centered")

st.title("📈 Kalkulator Untung Saham")
st.caption("Kira untung bersih & aliran tunai sebenar (Cashflow).")

# --- INPUT DATA ---
st.markdown("### 1. Masukkan Detail Trade")

col1, col2 = st.columns(2)

with col1:
    st.info("🟢 BUY (Beli)")
    buy_price = st.number_input("Harga Beli (RM)", value=0.500, step=0.005, format="%.3f")
    lot_size = st.number_input("Berapa Lot?", value=1, step=1, help="1 Lot = 100 Unit")
    
with col2:
    st.error("🔴 SELL (Jual)")
    sell_price = st.number_input("Harga Jual (RM)", value=0.550, step=0.005, format="%.3f")
    
    # Pilihan Broker
    broker_type = st.selectbox("Jenis Broker:", 
                               ["Min RM 8 (Standard)", "Cash Upfront (0.05%)", "Normal (0.42%)", "Tiada Kos (Paper Trade)"])

# --- FUNGSI KIRA KOS BURSA ---
def kira_kos(nilai_trade, jenis_broker):
    if jenis_broker == "Tiada Kos (Paper Trade)":
        return 0.0
    
    # 1. Brokerage Fee
    rate = 0.0
    min_fee = 0.0
    
    if "0.05%" in jenis_broker: rate = 0.0005 
    elif "0.42%" in jenis_broker: rate = 0.0042 
    elif "Min RM 8" in jenis_broker: 
        rate = 0.0042 
        min_fee = 8.00
        
    brokerage = max(nilai_trade * rate, min_fee)
    
    # 2. Clearing Fee (0.03% max RM1000)
    clearing = min(nilai_trade * 0.0003, 1000.0)
    
    # 3. Stamp Duty (RM1.50 per RM1000, max RM1000)
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

# Kira Kos
kos_beli = kira_kos(nilai_beli_kasar, broker_type)
kos_jual = kira_kos(nilai_jual_kasar, broker_type)
total_kos_transaksi = kos_beli + kos_jual

# ALIRAN TUNAI SEBENAR (TOTAL DUIT)
# Beli = Harga Saham + Kos (Kena bayar lebih)
total_duit_keluar = nilai_beli_kasar + kos_beli 

# Jual = Harga Saham - Kos (Dapat kurang)
total_duit_masuk = nilai_jual_kasar - kos_jual 

# Untung Bersih
untung_bersih = total_duit_masuk - total_duit_keluar
peratus_untung = (untung_bersih / total_duit_keluar) * 100 if total_duit_keluar > 0 else 0

# --- PAPARAN KEPUTUSAN ---
st.divider()

if st.button("🧮 Kira Total Duit", type="primary"):
    
    st.markdown("### 2. Keputusan Kewangan")
    
    # Tunjuk Aliran Tunai Besar-Besar
    k1, k2 = st.columns(2)
    k1.metric("💸 Total Duit KELUAR (Modal)", f"RM {total_duit_keluar:,.2f}", delta="- (Modal + Fee)", delta_color="inverse")
    k2.metric("💰 Total Duit MASUK (Pulangan)", f"RM {total_duit_masuk:,.2f}", delta=f"+ (Jual - Fee)")
    
    st.divider()
    
    # Status Untung Rugi
    if untung_bersih > 0:
        st.success(f"### 🎉 UNTUNG BERSIH: RM {untung_bersih:,.2f}")
        st.caption(f"ROI: +{peratus_untung:.2f}%")
        st.balloons()
    elif untung_bersih < 0:
        st.error(f"### 💸 RUGI BERSIH: RM {untung_bersih:,.2f}")
        st.caption(f"ROI: {peratus_untung:.2f}%")
    else:
        st.warning("### 😐 BALIK MODAL (Breakeven)")

    # Perincian Kos (Expendable)
    with st.expander("Tengok Breakdown Kos & Fee"):
        st.write(f"Harga Saham Semata-mata: RM {nilai_beli_kasar:,.2f}")
        st.write(f"Kos Beli (Broker+Tax): RM {kos_beli:.2f}")
        st.write(f"Kos Jual (Broker+Tax): RM {kos_jual:.2f}")
        st.write(f"**Total Fee Hangus:** RM {total_kos_transaksi:.2f}")

else:
    st.info("Tekan butang kira di atas.")
