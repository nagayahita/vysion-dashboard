
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Vysion CFO Tool", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #0f0f0f;
    }
    .stButton button {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #444;
        padding: 1em;
        font-weight: bold;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #262626;
        border: 1px solid #00d1b2;
    }
    .hero-box {
        background-color: #1a1a1a;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 10px #111;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("👑 Welcome to Vysion")
st.markdown("### The One-Man Finance System — Designed to Replace Your Entire Finance Division")

# Upload Excel
uploaded_file = st.file_uploader("📤 Upload Data Keuangan Anda (Excel)", type=["xlsx"])

if uploaded_file:
    df_income = pd.read_excel(uploaded_file, sheet_name="Pemasukan")
    df_expense = pd.read_excel(uploaded_file, sheet_name="Pengeluaran")

    total_income = df_income['Jumlah (Rp)'].sum()
    total_expense = df_expense['Jumlah (Rp)'].sum()
    net_cashflow = total_income - total_expense

    # Hero Box
    st.markdown('<div class="hero-box">', unsafe_allow_html=True)
    st.subheader("📊 Ringkasan Cashflow Bulan Ini")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", f"Rp{total_income:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp{total_expense:,.0f}")
    col3.metric("Net Cashflow", f"Rp{net_cashflow:,.0f}", delta_color="inverse")

    # Grafik
    df_income['Type'] = 'Pemasukan'
    df_expense['Type'] = 'Pengeluaran'
    df_all = pd.concat([df_income, df_expense])
    df_all['Tanggal'] = pd.to_datetime(df_all['Tanggal'])
    df_grouped = df_all.groupby(['Tanggal', 'Type'])['Jumlah (Rp)'].sum().unstack(fill_value=0)
    df_grouped['Net Cashflow'] = df_grouped['Pemasukan'] - df_grouped['Pengeluaran']

    st.line_chart(df_grouped[['Pemasukan', 'Pengeluaran', 'Net Cashflow']])
    st.markdown('</div>', unsafe_allow_html=True)

# Modular Buttons
st.subheader("🔎 Navigasi Fitur Vysion")

colA, colB, colC = st.columns(3)
with colA:
    if st.button("📘 Modul Akuntansi"):
        st.switch_page("pages/3_Modul_Akuntansi.py")
with colB:
    if st.button("🧠 AI Insight"):
        st.switch_page("pages/2_AI_Insights.py")
with colC:
    if st.button("📤 Export Laporan"):
        st.switch_page("pages/4_Export_Report.py")
