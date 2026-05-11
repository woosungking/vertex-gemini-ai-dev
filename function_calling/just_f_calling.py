from google import genai
from google.genai import types

PROJECT_ID = "vertexailab-495605"
LOCATION = "us-central1"
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# 모델이 이해할 수 있도록 Docstring을 정성껏 적어주는 것이 포인트입니다.
def get_landmarks(location: str) -> dict:
    """주어진 지역의 랜드마크 정보를 가져옵니다.
    
    Args:
        location: 도시 이름 (예: 서울, 뉴욕)
    """
    if "서울" in location:
        return {"landmark": "기무성"}
    return {"landmark": "정보가 없습니다."}

# 자동 호출 설정을 넣어줍니다.
config = types.GenerateContentConfig(
    tools=[get_landmarks],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="서울 랜드마크좀 알려줘",
    config=config,
)

for part in response.candidates[0].content.parts:
    if part.function_call:
        print(f"함수 호출 요청됨: {part.function_call.name}")
        print(f"전달된 인자: {part.function_call.args}")
    if part.text:
        print(f"최종 답변: {part.text}")