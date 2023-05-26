import streamlit as st
from streamlit_chat import message # chat bot을 만들기 쉬운 library
from audiorecorder import audiorecorder # audio 인식을 위한 library
import requests
import io

# session state init
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
    # [{"role": "user", "content": "~~~"}, {"role": "assistant", "content": "~~1221~"}] 형태

host_url = "http://127.0.0.1:8000"
chat_url = f"{host_url}/chat"
transcribe_url = f"http://127.0.0.1:8000/transcribe"

# chat gpt part
def chat(text):
    user_turn = {"role": "user", "content": text}
    messages = st.session_state['messages']
    response = requests.post(chat_url, json={"messages": messages + [user_turn]})
    assistant_turn = response.json()
    
    st.session_state['messages'].append(user_turn)
    st.session_state['messages'].append(assistant_turn)

# speech to text part
def speach_to_text(audio_bytes):
    audio_file = io.BytesIO(audio_bytes)
    files = {"audio_file": ("audio.wav", audio_file, "audio/wav")}
    response = requests.post(transcribe_url, files=files)
    text = response.json()['text']
    return text
    
st.title("챗봇 서비스")

# UI 순서 배치를 위해
raw1 = st.container()
raw2 = st.container()
    
with raw2:
    # 입력 부분   
    # input_text = st.text_input("You")
    # if input_text:
    #    chat(input_text)    
        
    audio = audiorecorder("Click to record", "Recording...")
    if len(audio) > 0: # 결과가 있을 때,
        audio_bytes = audio.tobytes()
        st.audio(audio_bytes)
        
        text = speach_to_text(audio_bytes)
        chat(text)

with raw1: 
    # text 출력 부분   
    for i, message_object in enumerate(st.session_state['messages']):
        msg = message_object['content']
        
        # user 조절
        is_user = False
        if i % 2 == 0:
            is_user = True
            
        message(msg, is_user=is_user, key=f"chat_{i}") # key는 대화 순서 간의 중복 발생 x를 위한

