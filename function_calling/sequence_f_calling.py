from google import genai
from google.genai import types

import requests

# Vertex AI 클라이언트 초기화
PROJECT_ID = "vertexailab-495605"
LOCATION = "us-central1"
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

API_KEY = ""

def get_geocoding(location: str) -> dict | None:
    """
    사용자 질문에서 지역 이름을 추출하고 해당 장소의 위도 및 경도 정보를 가져옵니다.
    Args:
        location: 지역 이름
    Returns:
        lat: 지역의 위도
        lon: 지역의 경도
    """
    # Geocoding API URL
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"


    # API 요청에 필요한 파라미터
    params = {
        "q": location,
        "limit": 1,
        "appid": API_KEY
    }


    print(f"1. 도시 '{location}'의 좌표를 조회합니다...")
    try:
        response = requests.get(geo_url, params=params)
        response.raise_for_status()
       
        data = response.json()
        lat = data[0]['lat']
        lon = data[0]['lon']
        return {"lat": lat, "lon": lon}


    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return None
   
def get_weather_data(lat: float, lon: float) -> dict | None:
    """
    위도와 경도를 사용하여 현재 날씨를 조회합니다.
    Args:
        lat: 지역의 위도
        lon: 지역의 경도
    Returns:
        current_weather: 지역의 현재 날씨
    """
    # Current Weather API URL
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
   
    # API 요청에 필요한 파라미터
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",  # 온도를 섭씨(°C)로 받기
        "lang": "kr"        # 응답을 한국어로 받기
    }
   
    print("\n2. 해당 좌표의 현재 날씨를 조회합니다...")
    try:
        response = requests.get(weather_url, params=params)
        response.raise_for_status()
       
        weather_data = response.json()
        return {"current_weather": weather_data}


    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return None

#------------------------------------------------------------------------------------------------------------------------

config = types.GenerateContentConfig(
    tools=[get_geocoding, get_weather_data],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="서울의 현재 날씨 알려줘.",
    config=config,
)

print(response.text)
