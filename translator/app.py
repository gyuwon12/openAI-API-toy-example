import os
import openai
import streamlit as st

openai.api_key = os.getenv("OPENAI_API_KEY") # 환경 변수 이용 -> export로 내 KEY 설정해주기

# davinci--003 version
def translate_text_version1(text, src, tar):
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = f"Translate the following {src} text to {tar}:  {text}",
        max_tokens = 200,
        n = 1,
        temperature = 1)
    translated_text = response.choices[0].text.strip()
    return translated_text

# few - shot을 위해
parallel_example = {
        "한국어": ["오늘 날씨 어때?", "오늘부터 칸영화제가 시작될거야."],
        "영어": ["How is the weather today?", "The Cannes Film Festival will start today."],
        "일본어": ["今日の天気はどう？", "今日からカンヌ映画祭が始まります。"],
        "프랑스어": ["Quel temps fait-il aujourd'hui ?", "Le Festival du Film de Cannes va commencer aujourd'hui."]
}

# gpt 3.5 version
def translate_text_version2(text, src, tar):
    def build_fewshot(src_lagn, tar_lang):
        src_examples = parallel_example[src_lagn]
        tar_examples = parallel_example[tar_lang]
        
        # few shot exmaple 추가하기
        fewshot_messages = []
        for src, tar in zip(src_examples, tar_examples):
            fewshot_messages.append({"role": "user", "content": src})
            fewshot_messages.append({"role": "assistant", "content": tar})
        return fewshot_messages
    
    # prompt    
    system_instruction = f"assistant는 번역앱으로서 동작한다. {src}을 {tar}으로 적절하게 번역하고, 번역된 텍스트만 출련한다."
    
    fewshot_messages = build_fewshot(src_lagn=src, tar_lang=tar)
    
    messages = [{"role": "system", "content": system_instruction},
                *fewshot_messages,
                {"role": "user", "content": text}]
    
    # model
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    translated_text = response['choices'][0]['message']['content']
    return translated_text

# title
st.title("번역 서비스")

# text area
text = st.text_area("번역할 텍스트를 입력하세요", "")

# corpus index
src_language = st.selectbox("원본 언어", ["영어", "한국어", "일본어", "프랑스어"]) # 기본값이 index = 0이라 UI에 영어가 뜸
tar_language = st.selectbox("목표 언어", ["영어", "한국어", "일본어", "프랑스어"], index=1)

if st.button("번역"):
    # 번역 함수를 만들어서 (text, src, tar) => return translated_text 
    translated_text = translate_text_version2(text, src_language, tar_language)
    st.success(translated_text)
    