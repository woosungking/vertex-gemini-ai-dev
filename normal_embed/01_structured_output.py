from pydantic import BaseModel
from google import genai

# Vertex AI 모드로 클라이언트를 초기화합니다.
# (방금 터미널에 설정한 JSON 인증 파일을 바탕으로 자동으로 권한을 얻어옵니다!)
client = genai.Client(
    vertexai=True,
    project="vertexailab-495605", # GCP 프로젝트 ID (혹시 다르다면 수정해 주세요)
    location="us-central1"        # 모델을 호출할 리전 (보통 us-central1을 기본으로 많이 씁니다)
)

# 2. 원하는 데이터 형태(스키마) 정의
class Recipe(BaseModel):
    recipe_name: str
    ingredients: list[str]

# 3. 모델 호출 (JSON 스키마 강제)
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="볶음밥 레시피를 알려줘",
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    }
)

# 4. 결과 확인
print(response.text)