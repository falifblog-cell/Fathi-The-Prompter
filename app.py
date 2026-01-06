import streamlit as st
import math

# --- SETUP ---
st.set_page_config(page_title="Kalkulator Saham Fathi", page_icon="📈", layout="centered")

st.title("📈 Kalkulator Untung Saham")
st.caption("Kira untung bersih & aliran tunai sebenar (Cashflow).")

# --- BAHAGIAN 1: INPUT DATA ---
st.markdown("### 1. Masukkan Detail Trade")

col1, col2 = st.columns(2)

# --- KOLUM BELI (KIRI) ---
with col1:
    st.info("🟢 BUY (Beli)")
    buy_price = st.number_input("Harga Beli (RM)", value=0.500, step=0.005, format="%.3f")
    lot_size = st.number_input("Berapa Lot?", value=1, step=1, help="1 Lot = 100 Unit")
    
    # KIRA TERUS NILAI KASAR BELI
    total_beli_raw = buy_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :green[RM {total_beli_raw:,.2f}]")

# --- KOLUM JUAL (KANAN) ---
with col2:
    st.error("🔴 SELL (Jual)")
    sell_price = st.number_input("Harga Jual (RM)", value=0.550, step=0.005, format="%.3f")
    
    # Kita anggap jual jumlah lot yang sama
    st.write(f"Jual: {lot_size} Lot") 
    
    # KIRA TERUS NILAI KASAR JUAL
    total_jual_raw = sell_price * lot_size * 100
    st.markdown(f"**Nilai Saham:** :red[RM {total_jual_raw:,.2f}]")

# PILIHAN BROKER (Duduk tengah-tengah)
st.divider()
broker_type = st.selectbox("Jenis Broker & Fee:", 
                           ["Min RM 8 (Standard)", "Cash Upfront (0.05%)", "Normal (0.42%)", "Tiada Kos (Paper Trade)"])


# --- FUNGSI KIRA KOS (LOGIK MATEMATIK) ---
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
    # Formula: Round up setiap 1000
    stamp = math.ceil(nilai_trade / 1000) * 1.50
    stamp = min(stamp, 1000.0)
    
    # 4. SST (8% atas Brokerage sahaja)
    sst = brokerage * 0.08
    
    total_kos = brokerage + clearing + stamp + sst
    return total_kos

# --- LOGIC PENGIRAAN AKHIR ---
unit_total = lot_size * 100
nilai_beli_kasar = buy_price * unit_total
nilai_jual_kasar = sell_price * unit_total

# Kira Kos
kos_beli = kira_kos(nilai_beli_kasar, broker_type)
kos_jual = kira_kos(nilai_jual_kasar, broker_type)
total_kos_transaksi = kos_beli + kos_jual

# Kira Aliran Tunai
total_duit_keluar = nilai_beli_kasar + kos_beli 
total_duit_masuk = nilai_jual_kasar - kos_jual 
untung_bersih = total_duit_masuk - total_duit_keluar
peratus_untung = (untung_bersih / total_duit_keluar) * 100 if total_duit_keluar > 0 else 0


# --- BAHAGIAN 2: KEPUTUSAN ---
st.divider()

if st.button("🧮 Kira Untung Bersih (Net Profit)", type="primary"):
    
    st.markdown("### 2. Keputusan Kewangan")
    
    # Tunjuk Aliran Tunai Besar-Besar
    k1, k2 = st.columns(2)
    k1.metric("💸 Modal Kena Ada (Total)", f"RM {total_duit_keluar:,.2f}", delta="- Termasuk Fee")
    k2.metric("💰 Duit Dapat Bersih", f"RM {total_duit_masuk:,.2f}", delta="+ Lepas Tolak Fee")
    
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

    # Perincian Kos
    with st.expander("Tengok Breakdown Kos"):
        st.write(f"Harga Saham (Raw): RM {nilai_beli_kasar:,.2f}")
        st.write(f"Total Fee Broker (Beli+Jual): RM {total_kos_transaksi:.2f}")
