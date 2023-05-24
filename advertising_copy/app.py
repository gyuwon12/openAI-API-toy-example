import streamlit as st
import requests # front - end에서 fast api 가져오려는

st.title("광고문구 작성 서비스")

generate_ad_copy_url = "http://127.0.0.1:8000/create_ad_copy"

product_name = st.text_input("제품 이름")
details = st.text_input("주요 내용")
options = st.multiselect("광고 문구의 톤앤 매너", options=["기본", "과장스럽게", "차분한", "웃긴"], default=["기본"])

if st.button("광고 문구 생성"):
    try:
        response = requests.post(generate_ad_copy_url, # requests.post() 함수를 사용하여 FastAPI 서버에 HTTP POST 요청을 보냄
                    json={"product_name": product_name, # 요청 본문에는 사용자가 입력한 product_name, details, options 값을 json 형식으로 전달
                            "details": details,
                            "tone_and_manner": ', '.join(options)})
        
        ad_copy = response.json()['ad_copy'] # 서버로부터 받은 응답을 json 형식으로 파싱하여 ad_copy 변수에 광고 문구를 저장
        st.success(ad_copy)
    except:
        st.error("예상치 못한 에러가 발생했습니다.")