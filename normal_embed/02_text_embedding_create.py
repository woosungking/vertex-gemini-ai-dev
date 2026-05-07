from google import genai
from google.genai.types import EmbedContentConfig

client = genai.Client(
    vertexai=True,
    project="vertexailab-495605", 
    location="global" 
)

texts_to_embed = [
    "운전면허증은 어떻게 받나요",
    "운전면허증은 얼마나 유효한가요",
    "운전면허 지식 테스트 학습 가이드"
]

embedding_config = EmbedContentConfig(
    task_type="RETRIEVAL_DOCUMENT",
    output_dimensionality=768,
)

response = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts_to_embed,
    config=embedding_config
)

print(f"생성된 임베딩 개수 : {len(response.embeddings)}")