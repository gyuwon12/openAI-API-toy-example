import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

system_instruction = """
너는 햄버거 가게 AI 비서야.

아래는 햄버거 종류야. 아래 종류의 버거 말고는 다른 버거는 없어.

- 빅맥 : 5000원
- 상하이 치즈 버거 : 6000원
- 불고기 버거 : 4500원

위 메뉴 말고는 없다고 생각하면 돼.
"""

messages=[{"role": "system", "content": system_instruction}]

def ask(text):
    # 질문 부분
    user_input = {"role": "user", "content": text}
    messages.append(user_input)
    
    # 답변 생성 부분
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
    )
    
    # 답변 필요한 부분 추출
    response = response.to_dict_recursive()
    bot_text = response['choices'][0]['message']['content']
    
    # 업데이트를 위해 추가
    assistant_input = {"role": "assistant", "content": bot_text}
    messages.append(assistant_input)
    
    return bot_text

while True:
    user_input = input("입력하세요: ")
    bot_resp = ask(user_input)
    
    print('='*20)
    print(f"user_input: {user_input}")
    print(f"chatbot_response: {bot_resp}")
