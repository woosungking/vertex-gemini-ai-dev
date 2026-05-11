from google import genai
from google.genai import types

PROJECT_ID = "vertexailab-495605"
LOCATION = "us-central1"
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


def brew_coffee(strength: str) -> dict:

    """
    지정된 농도로 커피를 내립니다.
    Args:
        strength: 커피 농도 ('진하게' 또는 '부드럽게')
    Returns:
        status: 현재 커피 상태를 나타냅니다.
    """
    return {"status": f"{strength} 커피를 내리고 있습니다."}

def get_daily_briefing(topics: list[str] = ["news", "weather"]) -> dict:

    """
    지정된 주제에 대한 일일 브리핑을 가져옵니다.
    Args:
        topics: 브리핑에 포함할 주제 목록
    Returns:
        briefing_topics: 브리핑 주제
    """

    return {"briefing_topics": topics}

def set_thermostat(temperature_celsius: float = 22.0) -> dict:
    """
    실내 온도를 조절합니다.
    Args:
        temperature_celsius: 목표 온도 (섭씨)
    Returns:
        temperature: 온도 설정값.
    """
    return {"temperature": f"{temperature_celsius}°C"}

config = types.GenerateContentConfig(
    system_instruction="사용자의 모닝 루틴을 위해 필요한 모든 도구를 호출하세요.",
    tools=[brew_coffee, get_daily_briefing, set_thermostat],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="좋은 아침! 하루를 시작할 준비를 해줘. 커피는 부드럽게~",
    config=config,
)
for part in response.candidates[0].content.parts:
    if part.function_call:
        print(f"함수 호출 요청됨: {part.function_call.name}")
        print(f"전달된 인자: {part.function_call.args}")
    if part.text:
        print(f"최종 답변: {part.text}")
print(response.text)


