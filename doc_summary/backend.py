import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel

openai.api_key = os.getenv("OPENAI_API_KEY") # 환경 변수 이용 -> export로 내 KEY 설정해주기

def chatgpt_summarize(text):
    system_instruction = "assistant는 user의 입력을 bullet point로 3줄 요약해준다."
    messages = [{"role": "system", "content": system_instruction},
                {"role": "user", "content": text}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    result = response['choices'][0]['message']['content']
    return result

app = FastAPI()

class InputText(BaseModel):
    text: str
    
@app.post("/summarize")
def summarize(input_text: InputText):
    summary = chatgpt_summarize(input_text.text)
    return {"summary": summary}

