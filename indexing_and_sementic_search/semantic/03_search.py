"""
STEP 3. 시맨틱 검색
  - 사용자 질문을 벡터화
  - Vector Search에서 유사한 FAQ 검색
  - 결과 출력

프로비저닝(1번)과 인덱싱(2번)이 완료된 후 실행하세요.
"""

from typing import List
from google import genai
from google.genai.types import EmbedContentConfig
from google.cloud import aiplatform
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    PROJECT_ID, LOCATION,
    EMBEDDING_MODEL, EMBEDDING_DIM,
    INDEX_ENDPOINT_ID, DEPLOYED_INDEX_ID,
)
from faq import faq_data_raw

# FAQ ID → 원문 텍스트 빠른 조회용
FAQ_MAP = {item["id"]: item["text"] for item in faq_data_raw}


def search(query_text: str, num_neighbors: int = 3) -> None:
    genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    # 질문 벡터화
    response_emb = genai_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[query_text],
        config=EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIM,
        ),
    )
    query_emb: List[float] = response_emb.embeddings[0].values

    # 유사도 검색
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=INDEX_ENDPOINT_ID
    )
    response = endpoint.find_neighbors(
        deployed_index_id=DEPLOYED_INDEX_ID,
        queries=[query_emb],
        num_neighbors=num_neighbors,
    )

    # 결과 출력
    print(f"\n검색어: '{query_text}'")
    print(f"{'─' * 50}")
    if not response or not response[0]:
        print("검색 결과가 없습니다.")
        print(f"{'─' * 50}")
        return
    for rank, neighbor in enumerate(response[0], start=1):
        faq_text = FAQ_MAP.get(neighbor.id, "(텍스트 없음)")
        print(f"[{rank}위] ID: {neighbor.id} | 유사도: {neighbor.distance:.4f}")
        print(f"      {faq_text}")
    print(f"{'─' * 50}")


def run():
    query = input("\n검색할 질문을 입력하세요: ").strip()
    if not query:
        print("질문을 입력해주세요.")
        return
    search(query)
