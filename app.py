import streamlit as st
from langchain.messages import HumanMessage
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import requests

load_dotenv()

@tool
def get_currency() -> str :
    "Frankfurter API를 사용하여 USD 대비 KRW(원화) 환율 조회"
    url = "https://api.frankfurter.dev/v1/latest?base=USD&symbols=KRW"

    try:
        response = requests.get(url)
        response.raise_for_status() # 에러 발생 시 예외 처리
        data = response.json()

        # 결과 출력
        date = data.get("date")
        rate = data.get("rates", {}).get("KRW")

        return f"[기준일자] {date}, [원/달러 환율] 1 USD = {rate:,.2f} KRW"
    except Exception as e:
        return f"환율 정보를 가져오는 중 오류가 발생했습니다: {e}"

if "agent" not in st.session_state :
    model = init_chat_model("gpt-5.5")
    st.session_state.agent = create_agent(model, tools = [get_currency], checkpointer=InMemorySaver())

if "messages" not in st.session_state :
    st.session_state.messages = []

st.title("실시간 환율 조회 에이전트")

prompt = st.chat_input("무엇이든 물어보세요")
if prompt:
    # response = model.invoke(prompt)
    response = st.session_state.agent.invoke(
        {"messages" : [HumanMessage(prompt)]},
        {"configurable" : {"thread_id" : "1"}}
    )
    st.session_state.messages.append({"role" : "user", "content" : prompt})
    st.session_state.messages.append({"role" : "ai", "content" : response['messages'][-1].content})

for message in st.session_state.messages :
    with st.chat_message(message['role']) :
        st.write(message['content'])