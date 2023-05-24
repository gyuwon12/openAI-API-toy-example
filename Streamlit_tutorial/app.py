import streamlit as st

#st.title("Title")
#st.write("this is text")

# 주석 사용으로 했는데, 마크다운으로 취급을 해서, 웹 페이지에 노출하나봄.
"""
# This is title
## This is subtitle

- first
- second
- third

wow ~
"""

text = st.text_input("text_input")
st.write(text)

selected = st.checkbox("개인정보 사용에 동의하시겠습니까?")
if selected: # 선택시 true 값을 내놓음
    st.success("동의했습니다.")
    
market = st.selectbox('시장', ('코스닥', '코스피', '나스닥'))
st.write(f"seleted market: {market}")

options = st.multiselect('종목',
                        ['apple', 'naver', 'microsoft'])

st.write(', '.join(options)) # list 형식의 출력

st.metric(label="네이버", value="200000원", delta="1000원")