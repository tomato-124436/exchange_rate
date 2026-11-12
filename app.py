import requests
import streamlit as st

st.title("💱 실시간 환율 조회 앱")
st.write("Frankfurter API를 활용한 간단한 환율 계산기야.")

# 통화 선택 옵션
currencies = ["USD", "EUR", "GBP", "JPY", "KRW", "CAD", "AUD"]

col1, col2 = st.columns(2)
with col1:
  base_currency = st.selectbox("기준 통화", currencies, index=0)  # 기본 USD
with col2:
  target_currency = st.selectbox(
      "변환할 통화", currencies, index=4
  )  # 기본 KRW

# 금액 입력
amount = st.number_input(
    "금액 입력", value=1.0, min_value=0.0, step=1.0
)

# 조회 버튼
if st.button("환율 계산하기"):
  if base_currency == target_currency:
    st.warning("기준 통화와 변환할 통화가 같아!")
  else:
    try:
      # Frankfurter API 호출
      url = f"https://api.frankfurter.app/latest?from={base_currency}&to={target_currency}"
      response = requests.get(url)
      data = response.json()

      if "rates" in data:
        rate = data["rates"][target_currency]
        result = amount * rate
        st.success(
            f"**{amount:,.2f} {base_currency}** = **{result:,.2f}"
            f" {target_currency}**"
        )
        st.caption(f"적용 환율: 1 {base_currency} = {rate:,.4f} {target_currency}")
      else:
        st.error("환율 정보를 가져오지 못했어.")
    except Exception as e:
      st.error(f"오류가 발생했어: {e}")
      