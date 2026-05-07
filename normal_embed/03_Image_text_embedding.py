import base64
from google import genai
from google.genai import types

# 1. Google Gen AI 클라이언트 초기화
# Vertex AI 백엔드 사용 (기존과 동일하게 GCP 프로젝트 인증 사용)
client = genai.Client(
    vertexai=True,
    project="vertexailab-495605",
    location="us-central1",
)

# 2. 이미지 로드 (가지고 계신 실제 이미지 파일 경로로 수정해 주세요!)
image_path = "effel.png"  # 예: "apple.png", "sample.jpg" 등

with open(image_path, "rb") as f:
    image_bytes = f.read()

# 3. 함께 벡터화할 텍스트 문맥 설정
text_context = "tower-effel"

# 4. 임베딩(벡터화) 실행
# gemini-embedding-2-preview: 이미지+텍스트+비디오+오디오를 하나의 통합 벡터 공간에 임베딩
# (구 multimodalembedding@001은 이미지/텍스트 벡터를 따로 반환했지만,
#  이 모델은 하나의 통합 벡터로 반환합니다)
print("벡터화 진행 중...")

# 텍스트 임베딩
text_response = client.models.embed_content(
    model="gemini-embedding-2-preview",
    contents=text_context,
)

# 이미지 임베딩
image_response = client.models.embed_content(
    model="gemini-embedding-2-preview",
    contents=types.Content(
        parts=[
            types.Part(
                inline_data=types.Blob(
                    mime_type="image/png",
                    data=image_bytes,
                )
            )
        ]
    ),
)

# 5. 결과 확인
print("✅ 벡터화 성공!")
print(f"텍스트 벡터 차원 수: {len(text_response.embeddings[0].values)}")
print(f"이미지 벡터 차원 수: {len(image_response.embeddings[0].values)}")

# (선택) 실제 생성된 벡터값 앞 5개만 살짝 확인해보기
print("텍스트 벡터값 샘플:", text_response.embeddings[0].values[:5])
print("이미지 벡터값 샘플:", image_response.embeddings[0].values[:5])
