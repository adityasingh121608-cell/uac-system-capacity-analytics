import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="HHS Care Load Analytics", page_icon="🏥", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_uac_analytics.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df_full = load_data()

st.title("🏥 System Capacity & Care Load Analytics")
st.markdown("**U.S. Department of Health & Human Services | Operational Healthcare Pipeline Monitor**")

st.sidebar.header("Filter Controls")
min_d = df_full['Date'].min().date()
max_d = df_full['Date'].max().date()

selected_range = st.sidebar.date_input("Select Date Range", [min_d, max_d], min_value=min_d, max_value=max_d)

if len(selected_range) == 2:
    start_d, end_d = selected_range
    df = df_full[(df_full['Date'].dt.date >= start_d) & (df_full['Date'].dt.date <= end_d)].copy()
else:
    df = df_full.copy()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Avg System Load", f"{int(df['Total_System_Load'].mean()):,}")
c2.metric("Peak System Load", f"{int(df['Total_System_Load'].max()):,}")
c3.metric("Net Intake Pressure", f"{int(df['Net_Intake'].sum()):,}")
c4.metric("Discharge Ratio", f"{df['Discharge_Offset_Ratio'].mean():.2f}x")
c5.metric("Volatility (Std Dev)", f"{df['Total_System_Load'].std():.1f}")

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Capacity & Trend Monitoring",
    "⚖️ CBP vs HHS Custody Share",
    "⚡ Inflow vs Outflow Balance",
    "📋 Raw Data Records"
])

with tab1:
    st.subheader("Total Care Load vs. Moving Averages")
    fig_load = go.Figure()
    fig_load.add_trace(go.Scatter(x=df['Date'], y=df['Total_System_Load'], name='Total Daily Load', line=dict(color='#2563eb', width=1.5)))
    fig_load.add_trace(go.Scatter(x=df['Date'], y=df['Load_7D_MA'], name='7-Day MA (Stress)', line=dict(color='#f97316', width=2)))
    fig_load.add_trace(go.Scatter(x=df['Date'], y=df['Load_14D_MA'], name='14-Day MA (Trend)', line=dict(color='#dc2626', width=2, dash='dash')))
    fig_load.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Active Child Count", hovermode="x unified")
    st.plotly_chart(fig_load, use_container_width=True)

with tab2:
    st.subheader("Custodial Share Over Time")
    fig_split = px.area(
        df, x='Date', y=['CBP_Custody', 'HHS_Care'],
        color_discrete_map={'CBP_Custody': '#f59e0b', 'HHS_Care': '#2563eb'},
        labels={'value': 'Children Count', 'variable': 'Facility Tier'},
        template="plotly_white"
    )
    st.plotly_chart(fig_split, use_container_width=True)

with tab3:
    st.subheader("Daily Intake vs. Placement Outflow")
    fig_flow = go.Figure()
    fig_flow.add_trace(go.Bar(x=df['Date'], y=df['Transfers_In_HHS'], name='Transfers into HHS', marker_color='#ef4444'))
    fig_flow.add_trace(go.Bar(x=df['Date'], y=df['HHS_Discharged'], name='Discharges / Placements', marker_color='#34d399'))
    fig_flow.add_trace(go.Scatter(x=df['Date'], y=df['Net_Intake'], name='Net Pressure', line=dict(color='#0f172a', width=2)))
    fig_flow.update_layout(barmode='group', template="plotly_white", xaxis_title="Date", yaxis_title="Daily Children Count", hovermode="x unified")
    st.plotly_chart(fig_flow, use_container_width=True)

with tab4:
    st.subheader("Validated Pipeline Dataset")
    st.dataframe(df, use_container_width=True)
