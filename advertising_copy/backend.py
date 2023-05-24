# fastapi aip server
# openai api를 활용해서 만든 광고 문구 작성 함수를 호출

import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel

openai.api_key = os.getenv("OPENAI_API_KEY") # 환경 변수 이용 -> export로 내 KEY 설정해주기

# Copy 생성기
class CopyGenerator():
    def __init__(self, model='gpt-3.5-turbo'):
        self.model = model
        self.infer_type = self._get_infer_type_by_model(model)
    
    # 모델 타입 정하기    
    def _get_infer_type_by_model(self, model): 
        if model.startswith("text-"): # 시작 이름 판단 -> 다빈치 모델이냐
            return 'completion'
        elif model.startswith("gpt-"): # chatgpt 모델이냐
            return 'chat'
        raise Exception(f"Unknown model type: {model}")
    
    # Type 1 -> Completion
    def _infer_using_completion(self, prompt):
        response = openai.Completion.create(
            model = self.model,
            prompt = prompt,
            max_tokens = 200,
            n = 1
        )
        result = response.choices[0].text.strip()
        return result
    
    # Type 2 -> ChatCompletion
    def _infer_using_chatcompletion(self, prompt):
        system_instruction = "assistantsms 광고 문구 작성 도우미로 작동한다. 'Copywriter'와 같은 존재야. user의 내용을 참고하여 광고 문구를 작성해라."
        messages = [{"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model = self.model,
            messages = messages
        )
        result = response['choices'][0]['message']['content']
        return result
        
    # Copy Generate 부분
    def generate(self, product_name, details, tone_and_manner):
        prompt = f"제품이름: {product_name}\n주요내용: {details}\n광고 문구의 스타일: {tone_and_manner}\n위 내용을 참고하여 마케팅 문구를 만들어라."
        if self.infer_type == 'completion':
            result = self._infer_using_completion(prompt=prompt)
        elif self.infer_type == 'chat':
            result = self._infer_using_chatcompletion(prompt=prompt)
        return result

# app(backend) 구현 부분
app = FastAPI()

class Product(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str
    
@app.post("/create_ad_copy")
def create_ad_copy(product: Product):
    copy_gen = CopyGenerator(model="gpt-3.5-turbo")
    
    ad_copy = copy_gen.generate(product_name=product.product_name,
                                details=product.details,
                                tone_and_manner=product.tone_and_manner)
    return {"ad_copy": ad_copy}