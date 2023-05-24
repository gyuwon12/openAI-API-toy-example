import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")

system_instruction = """
너는 햄버거 가게 AI 비서야.

아래는 햄버거 종류야. 아래 종류의 버거 말고는 다른 버거는 없어.

- 빅맥
- 상하이 치즈 버거
- 불고기 버거

위 메뉴 말고는 없다고 생각하면 돼.
"""

user_instruction_no1 = """
각가의 햄버거 가격은 얼마야?
"""

assistant_instruction_no1 = """
빅맥은 5000원, 상하이 치즈 버거는 6000원, 불고기 버거는 4500원입니다.
"""

user_instruction_no2 = """
민트 초코 버거를 신메뉴로 도입한다고 할 때, 가격을 얼마로 하는게 적당할까?
"""

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": system_instruction}, # The system message helps set the behavior of the assistant.
        {"role": "user", "content": user_instruction_no1},
        {"role": "assistant", "content": assistant_instruction_no1},
        {"role": "user", "content": user_instruction_no2}
    ]
)

#print(response) 
"""
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "The 2020 World Series was played at a neutral site due to the COVID-19 pandemic. It was played at Globe Life Field in Arlington, Texas.",
        "role": "assistant"
      }
    }
  ],
  "created": 1684734775,
  "id": "chatcmpl-7IslTj2ZuIiXALzhyp08LELV5WwDa",
  "model": "gpt-3.5-turbo-0301",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 32,
    "prompt_tokens": 57,
    "total_tokens": 89
  }
}
"""
# 원하는 정보만 얻어오기
# print(response['choices']['message']['content']) 자료형이 자체 자료형이라 바꿔줘야함
response = response.to_dict_recursive()
print(response['choices'][0]['message']['content'])

"""
민트 초코 버거는 일반적인 햄버거와는 맛과 컨셉이 다르기 때문에 가격을 새로 책정해야 합니다. 
하지만 먼저 시장에서 유사한 제품이 얼마정도에 판매되고 있는지, 소비자의 구매력과 가격 대비 만족도 등을 고려해야 합니다. 
일반적인 햄버거의 가격 대비로 생각하면 7000원~9000원 정도가 적당할 것으로 예상됩니다. 그러나 이 역시 시장 조사를 통해 결정하는 것이 좋습니다.
"""