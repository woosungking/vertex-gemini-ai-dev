"""
STEP 2. 프로비저닝
  - Vector Search 인덱스 생성 (GCS의 JSONL 읽어서 구축)
  - 엔드포인트 생성
  - 엔드포인트에 인덱스 배포

주의: 인덱스 생성은 10~20분 소요됩니다.
      최초 1회만 실행하면 됩니다.
      반드시 1번(인덱싱) 실행 후 GCS에 데이터가 있는 상태에서 실행하세요.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.cloud import aiplatform
from AI_Agent_Vector_Search.indexing_and_sementic_search.config import (
    PROJECT_ID, LOCATION,
    INDEX_DISPLAY_NAME, GCS_INPUT_URI,
    DEPLOYED_INDEX_ID, EMBEDDING_DIM,
)


def create_index() -> aiplatform.MatchingEngineIndex:
    print("[1/3] Vector Search 인덱스 생성 중... (10~20분 소요)")
    faq_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=INDEX_DISPLAY_NAME,
        contents_delta_uri=GCS_INPUT_URI,
        description="FAQ 데이터에 대한 벡터DB 입니다.",
        dimensions=EMBEDDING_DIM,
        approximate_neighbors_count=50,
        leaf_node_embedding_count=10,
        leaf_nodes_to_search_percent=20,
        distance_measure_type=aiplatform.matching_engine.matching_engine_index_config.DistanceMeasureType.DOT_PRODUCT_DISTANCE,
        index_update_method="BATCH_UPDATE",
    )
    print(f"✅ 인덱스 생성 완료: {faq_index.resource_name}")
    return faq_index


def create_endpoint() -> aiplatform.MatchingEngineIndexEndpoint:
    print("[2/3] 엔드포인트 생성 중...")
    faq_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
        display_name="faq_index_endpoint",
        public_endpoint_enabled=True,
    )
    print(f"✅ 엔드포인트 생성 완료: {faq_index_endpoint.resource_name}")
    return faq_index_endpoint


def deploy_index(
    faq_index: aiplatform.MatchingEngineIndex,
    faq_index_endpoint: aiplatform.MatchingEngineIndexEndpoint,
) -> None:
    print("[3/3] 엔드포인트에 인덱스 배포 중...")
    faq_index_endpoint.deploy_index(
        index=faq_index,
        deployed_index_id=DEPLOYED_INDEX_ID,
        min_replica_count=1,
    )
    print(f"✅ 배포 완료")
    print(f"\n📌 config.py의 INDEX_ENDPOINT_ID를 아래 값으로 업데이트하세요:")
    print(f"   {faq_index_endpoint.resource_name.split('/')[-1]}")


def run():
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    faq_index = create_index()
    faq_index_endpoint = create_endpoint()
    deploy_index(faq_index, faq_index_endpoint)

    print("\n✅ 프로비저닝 완료. 다음 단계: 3번(검색) 실행")
