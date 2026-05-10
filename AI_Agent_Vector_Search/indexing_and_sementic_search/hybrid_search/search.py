"""
하이브리드 검색 실행
  - Dense(의미) + Sparse(키워드) 벡터를 RRF 알고리즘으로 융합
  - 카테고리 필터 적용
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from google.cloud import aiplatform
from google.cloud.aiplatform.matching_engine.matching_engine_index_endpoint import (
    MatchNeighbor, Namespace, HybridQuery
)

from AI_Agent_Vector_Search.indexing_and_sementic_search.config import PROJECT_ID, LOCATION, INDEX_ENDPOINT_ID, FILTERED_DEPLOYED_INDEX_ID
from AI_Agent_Vector_Search.indexing_and_sementic_search.hybrid_search.embeddings import get_dense_embedding, get_sparse_embedding

# 하이브리드 검색 설정
RRF_ALPHA = 0.5    # Dense:Sparse 가중치 (0.5 = 5:5)
NUM_NEIGHBORS = 5  # 반환할 결과 개수


def execute_hybrid_search(
    query_text: str,
    category: str,
    rrf_alpha: float = RRF_ALPHA,
    num_neighbors: int = NUM_NEIGHBORS,
) -> List[MatchNeighbor]:
    """Dense + Sparse 하이브리드 검색 실행"""

    # 1. 질문을 두 가지 벡터로 변환
    dense_emb = get_dense_embedding(query_text)
    sparse_emb = get_sparse_embedding(query_text)

    # 2. 하이브리드 쿼리 객체 생성
    query = HybridQuery(
        dense_embedding=dense_emb,
        sparse_embedding_dimensions=sparse_emb["dimensions"],
        sparse_embedding_values=sparse_emb["values"],
        rrf_ranking_alpha=rrf_alpha,
    )

    # 3. 카테고리 필터
    category_filter = [Namespace(name="category", allow_tokens=[category], deny_tokens=[])]

    # 4. 검색 실행
    aiplatform.init(project=PROJECT_ID, location=LOCATION)
    endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=INDEX_ENDPOINT_ID
    )
    response = endpoint.find_neighbors(
        deployed_index_id=FILTERED_DEPLOYED_INDEX_ID,
        queries=[query],
        num_neighbors=num_neighbors,
        filter=category_filter,
    )
    return response
