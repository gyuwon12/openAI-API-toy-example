import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY") # 환경 변수 이용 -> export로 내 KEY 설정해주기

prompt_ver1 = """
다음 문장이 긍정이면 positive, 부정이면 negative를 만들어라.

text: 이 영화 최악이다
sentiment: negative

text: 배우들이 연기를 너무 잘하네
sentiment: positive

text: 다시 보고 싶은 영화에요.
sentiment: """

query = input("입력하세요: ")

prompt_ver2 = """
다음 문장이 긍정이면 positive, 부정이면 negative를 만들어라

text: 이 영화 최악이다
sentiment: negative

text: 배우들이 연기를 너무 잘하네
sentiment: positive

text: """

prompt_ver2 = prompt_ver2 + query + "\nsentiment: "

response = openai.Completion.create(model="text-davinci-003", # 라이브러리에 따라 모델 종류가 다름, API reference model overvie에서 확인할 것
                                    prompt=prompt_ver2, # instruction 부분
                                    temperature=0, # random : range(0,2)
                                    max_tokens=7) # response max length에 해당, openAI 토크나이저 기준이라 음절, 단어와 다른 개념인듯

#print(response)
"""
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "text": " positive" <- 여기가 Response
    }
  ],
  "created": 1684733727,
  "id": "cmpl-7IsUZQeutMSIwDiQrSungs22V1821",
  "model": "text-davinci-003",
  "object": "text_completion",
  "usage": {
    "completion_tokens": 1,
    "prompt_tokens": 163,
    "total_tokens": 164
  }
}
"""
# 원하는 출력만 가져오기
print(response['choices'][0]['text'])