"""
카테고리 필터링 버전 시맨틱 검색
  - 카테고리를 지정해서 해당 카테고리 FAQ만 검색
  - 카테고리 미지정 시 전체 검색
  - FILTERED_DEPLOYED_INDEX_ID 참조 (기존 인덱스와 분리)

사용 가능한 카테고리:
  account  - 계정, 로그인, 비밀번호
  payment  - 결제, 환불, 쿠폰, 포인트
  support  - 고객센터, 이벤트, 등급
  app      - 앱, 설치, 오류, 네트워크
  privacy  - 개인정보, 보안, 암호화
  dev      - API, SDK, Webhook
  service  - 서비스, 점검, 협업
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from google import genai
from google.genai.types import EmbedContentConfig
from google.cloud import aiplatform

from config import (
    PROJECT_ID, LOCATION,
    EMBEDDING_MODEL, EMBEDDING_DIM,
    INDEX_ENDPOINT_ID, FILTERED_DEPLOYED_INDEX_ID,
)
from faq_filtered_add import faq_data_filtered

VALID_CATEGORIES = ["account", "payment", "support", "app", "privacy", "dev", "service"]
FAQ_MAP = {item["id"]: item["text"] for item in faq_data_filtered}


def search(query_text: str, category: Optional[str] = None, num_neighbors: int = 3) -> None:
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

    restricts = None
    if category:
        restricts = [{"namespace": "category", "allow": [category]}]

    response = endpoint.find_neighbors(
        deployed_index_id=FILTERED_DEPLOYED_INDEX_ID,  # 필터링 인덱스 참조
        queries=[query_emb],
        num_neighbors=num_neighbors,
        restricts=restricts,
    )

    # 결과 출력
    category_label = f"[카테고리: {category}]" if category else "[전체]"
    print(f"\n검색어: '{query_text}' {category_label}")
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

    print(f"\n카테고리를 선택하세요 (Enter 입력 시 전체 검색):")
    for cat in VALID_CATEGORIES:
        print(f"  {cat}")
    category = input("카테고리: ").strip() or None

    if category and category not in VALID_CATEGORIES:
        print(f"유효하지 않은 카테고리입니다. 전체 검색으로 진행합니다.")
        category = None

    search(query, category)


if __name__ == "__main__":
    run()
