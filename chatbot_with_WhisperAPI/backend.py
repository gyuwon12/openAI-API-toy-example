import os
import openai
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

openai.api_key = os.getenv("OPENAI_API_KEY") # 환경 변수 이용 -> export로 내 KEY 설정해주기.

def chat(messages):
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    # {"role": "assistant", "content": "~~~"}
    response_dict = response.to_dict_recursive() # openai만의 자료형을 dict 자료형으로 변환
    assistant_turn = response_dict['choices'][0]['message']
    return assistant_turn

class Turn(BaseModel):
    role: str
    content: str

class Messages(BaseModel):
    messages: list[Turn] # [{"role": "user", "content": "~~~"}, {"role": "assistant", "content": "~~1221~"}] 요런 자료형을 다루기 위함
 
app = FastAPI() 
    
@app.post("/chat", response_model=Turn) # response_model은 응답 성공시 나올 자료형 표기
def post_chat(messages: Messages):
    chat_input_messages = messages.dict()
    assistant_turn = chat(messages=chat_input_messages['messages'])
    return assistant_turn

# with WhisperAPI
@app.post("/transcribe")
def transcribe_audio(audio_file: UploadFile = File(...)):
    # 혹시 모르니.
    try:
        file_name = "tmp_audio_file.wav"
        with open(file_name, "wb") as f:
            f.write(audio_file.file.read())
        
        with open(file_name, "rb") as f:
            transcription = openai.Audio.transcribe("whisper-1", f)
        
        text = transcription['text']
        
    except Exception as e:
        print(e)
        text = f"음성인식에서 실패했습니다. {e}"

    return {"text": text}