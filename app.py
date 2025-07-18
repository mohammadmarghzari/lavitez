import streamlit as st
from laevitas import Laevitas
import plotly.graph_objects as go

# --- عنوان و تنظیمات اولیه ---
st.set_page_config(page_title="ETH OI Change", layout="wide")
st.title("📊 نمودار تغییرات Open Interest برای ETH (Laevitas + Deribit)")

# --- گرفتن API KEY از کاربر ---
api_key = st.text_input("🔑 کلید API خود را وارد کنید:", type="password")

if api_key:
    try:
        lv = Laevitas(api_key=api_key)

        # --- گرفتن لیست تاریخ‌های سررسید ---
        expiries = lv.derivatives.option_expiries(
            underlying="ETH", exchange="deribit", currency="USD"
        )
        expiry = st.selectbox("📅 انتخاب تاریخ سررسید:", expiries)

        # --- گرفتن داده‌ها ---
        response = lv.derivatives.option_chain_oi_change(
            underlying="ETH",
            exchange="deribit",
            expiry=expiry,
            currency="USD"
        )

        # --- پردازش داده‌ها ---
        calls = [item for item in response if item['optionType'] == 'call']
        puts = [item for item in response if item['optionType'] == 'put']

        strike_calls = [item['strike'] for item in calls]
        oi_change_calls = [item['oiChange'] for item in calls]

        strike_puts = [item['strike'] for item in puts]
        oi_change_puts = [item['oiChange'] for item in puts]

        # --- رسم نمودار ---
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=strike_calls, y=oi_change_calls,
            name='Call OI Change', marker_color='green'
        ))
        fig.add_trace(go.Bar(
            x=strike_puts, y=oi_change_puts,
            name='Put OI Change', marker_color='red'
        ))

        fig.update_layout(
            title=f'ETH Open Interest Change by Strike - {expiry}',
            xaxis_title='Strike Price',
            yaxis_title='OI Change',
            barmode='group',
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ خطا در اتصال یا پردازش داده‌ها: {e}")
else:
    st.warning("🔒 لطفاً ابتدا کلید API خود را وارد کنید.")
