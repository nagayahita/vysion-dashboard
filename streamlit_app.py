
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="Vysion CFO AI", layout="wide")
st.title("📊 Vysion – Smart Financial Insight Dashboard")

# Upload file
uploaded_file = st.file_uploader("Upload File Excel Template Vysion", type=["xlsx"])
if uploaded_file:
    df_income = pd.read_excel(uploaded_file, sheet_name="Pemasukan")
    df_expense = pd.read_excel(uploaded_file, sheet_name="Pengeluaran")

    # Ringkasan
    total_income = df_income['Jumlah (Rp)'].sum()
    total_expense = df_expense['Jumlah (Rp)'].sum()
    net_cashflow = total_income - total_expense

    st.subheader("💰 Ringkasan Finansial")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", f"Rp{total_income:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp{total_expense:,.0f}")
    col3.metric("Net Cashflow", f"Rp{net_cashflow:,.0f}", delta_color="inverse")

    # Grafik cashflow
    df_income['Type'] = 'Pemasukan'
    df_expense['Type'] = 'Pengeluaran'
    df_all = pd.concat([df_income, df_expense])
    df_all['Tanggal'] = pd.to_datetime(df_all['Tanggal'])
    df_grouped = df_all.groupby(['Tanggal', 'Type'])['Jumlah (Rp)'].sum().unstack(fill_value=0)
    df_grouped['Net Cashflow'] = df_grouped['Pemasukan'] - df_grouped['Pengeluaran']

    st.subheader("📈 Grafik Arus Kas")
    st.bar_chart(df_grouped[['Pemasukan', 'Pengeluaran', 'Net Cashflow']])

    # Insight Otomatis
    st.subheader("💡 Insight Otomatis dari AI")

    insights = []
    insights.append(f"📅 {datetime.today().strftime('%d %B %Y')}")

    if net_cashflow > 0:
        insights.append(f"✅ Arus kas bersih Anda positif sebesar Rp{net_cashflow:,.0f}.")
    else:
        insights.append(f"⚠️ Arus kas bersih Anda negatif sebesar Rp{abs(net_cashflow):,.0f}. Segera tinjau pengeluaran!")

    mean_exp = df_expense['Jumlah (Rp)'].mean()
    threshold = mean_exp * 1.5
    anomaly_expense = df_expense[df_expense['Jumlah (Rp)'] > threshold]

    if not anomaly_expense.empty:
        for _, row in anomaly_expense.iterrows():
            insights.append(f"🚨 Pengeluaran tidak wajar: {row['Deskripsi']} - Rp{row['Jumlah (Rp)']:,.0f}")

    if total_expense > total_income * 0.7:
        insights.append("⚠️ Pengeluaran melebihi 70% dari pemasukan. Perlu efisiensi.")
    else:
        insights.append("✅ Proporsi pengeluaran masih dalam batas aman.")

    for text in insights:
        st.write(text)
