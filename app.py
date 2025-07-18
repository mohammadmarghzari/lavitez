import streamlit as st
from laevitas import Laevitas
import plotly.graph_objects as go

st.set_page_config(page_title="ETH OI Change by Laevitas", layout="wide")
st.title("📊 ETH Open Interest Change Dashboard")

api_key = st.text_input("🔑 Enter your Laevitas API Key:", type="password")

if api_key:
    lv = Laevitas(api_key=api_key)
    try:
        expiries = lv.derivatives.option_expiries(underlying="ETH", exchange="deribit", currency="USD")
        expiry = st.selectbox("📅 Choose expiry date:", expiries)

        response = lv.derivatives.option_chain_oi_change(
            underlying="ETH", exchange="deribit", expiry=expiry, currency="USD"
        )

        calls = [item for item in response if item.get("optionType") == "call"]
        puts  = [item for item in response if item.get("optionType") == "put"]

        if calls or puts:
            strike_calls = [item["strike"] for item in calls]
            oi_calls     = [item["oiChange"] for item in calls]
            strike_puts = [item["strike"] for item in puts]
            oi_puts     = [item["oiChange"] for item in puts]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=strike_calls, y=oi_calls, name="Call OI Change", marker_color="green"))
            fig.add_trace(go.Bar(x=strike_puts, y=oi_puts, name="Put OI Change", marker_color="red"))

            fig.update_layout(title=f"ETH OI Change by Strike – {expiry}",
                              xaxis_title="Strike Price",
                              yaxis_title="OI Change",
                              barmode="group",
                              height=600)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ هیچ داده‌ای برای این تاریخ پیدا نشد.")

    except Exception as e:
        st.error(f"❌ خطا در دریافت داده یا رسم نمودار:\n{e}")
else:
    st.warning("🔐 لطفاً ابتدا API Key خود را وارد کنید.")
