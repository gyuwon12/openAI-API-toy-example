import streamlit as st
import requests
import pandas as pd
import os
import io

# stremalit은 정보가 '다운로드'와 같은 변경이 되면 코드를 처음부터 다시 실행하게 되는데, 이 때 변수들의 정보들이 다 날아가게 됨.
# 문액 유지를 위해 아래 기능이 필요, 이전에 업로드 된/만들어진 데이터 프레임 기억을 위해서.
# 아래는 session_state init 개념
if 'prev_uploaded_file' not in st.session_state:
    st.session_state['prev_uploaded_file'] = None
    st.session_state['prev_df'] = None

summarize_url = "http://127.0.0.1:8000/summarize"

# 입력값 요약 기본 tool
def doc_summarize(text):
    response = requests.post(summarize_url,
                             json={"text": text})
    summary = response.json()["summary"]
    return summary

# 엑셀 파일 요약 부분 -> tab2
def summarize_dataframe(df): 
    global progress_bar
    
    total = len(df) # 헤더 제외 개수를 내보냄
    new_summary = [] # summary 모음집
    for i, news_origin in enumerate(df['뉴스원문'], start=1): # '뉴스원문' column 가져오기
        summary = doc_summarize(news_origin)
        new_summary.append(summary)
        progress_bar.progress(i/total, text="progress")
        
    df['뉴스요약'] = new_summary
    return df   

# data frame -> 엑셀 변환 api라고 생각
def to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

st.title("문서 요약 서비스")
tab1, tab2 = st.tabs(["실시간", "파일업로드"])
    
with tab1:
    input_text = st.text_area("여기에 문서를 입력해주세요.", height=300)
    if st.button("요약"):
        if input_text:
            try:
                summary = doc_summarize(input_text)
                st.success(summary)
            except:
                st.error("요청에 오류가 발생했습니다.")
        else:
            st.warning("텍스트를 입력하세요.")
            
with tab2:
    upload_file = st.file_uploader("파일을 선택하세요.")
    
    if upload_file:
        st.success("업로드 성공")
        
        # 이미 session_staet에 저장되어 있으면 기억장치에서 불러오는 개념
        if upload_file == st.session_state['prev_uploaded_file']:
            df = st.session_state['prev_df']
        # 없으면(즉, 처음이라면) session_stae에 저장해주는 개념
        else:
            # 처리 확인
            progress_bar = st.progress(0, text="progress")
            
            # 요약 전
            df = pd.read_excel(upload_file)
            
            # 요약문 추가 과정, 요약 후
            """요약 후"""
            df = summarize_dataframe(df)
            st.dataframe(df)
            
            # session_state 저장 개념
            st.session_state['prev_uploaded_file'] = upload_file
            st.session_state['prev_df'] = df

        file_base_name = os.path.splitext(os.path.basename(upload_file.name))[0]
        st.download_button(
            label="다운로드",
            data=to_excel(df),
            file_name=f"{file_base_name}__summarized.xlsx"
        )