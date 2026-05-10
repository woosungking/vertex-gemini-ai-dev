"""
카테고리 필터링 버전 프로비저닝
  - 기존 인덱스(faq_index)와 별개로 새 인덱스(faq_filtered_index) 생성
  - 기존 엔드포인트에 추가 배포 (엔드포인트 재사용)
  - GCS 경로: Vector_Search/FAQ_filtered (기존과 다른 경로)

최초 1회만 실행하면 됩니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.cloud import aiplatform
from AI_Agent_Vector_Search.indexing_and_sementic_search.config import (
    PROJECT_ID, LOCATION,
    FILTERED_INDEX_DISPLAY_NAME, GCS_FILTERED_INPUT_URI,
    FILTERED_DEPLOYED_INDEX_ID, EMBEDDING_DIM,
    INDEX_ENDPOINT_ID,
)


def create_filtered_index() -> aiplatform.MatchingEngineIndex:
    print("[1/2] 필터링 인덱스 생성 중... (10~20분 소요)")
    faq_filtered_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
        display_name=FILTERED_INDEX_DISPLAY_NAME,
        contents_delta_uri=GCS_FILTERED_INPUT_URI,  # 별도 GCS 경로
        description="카테고리 필터링이 적용된 FAQ 벡터DB입니다.",
        dimensions=EMBEDDING_DIM,
        approximate_neighbors_count=50,
        leaf_node_embedding_count=10,
        leaf_nodes_to_search_percent=20,
        distance_measure_type=aiplatform.matching_engine.matching_engine_index_config.DistanceMeasureType.DOT_PRODUCT_DISTANCE,
        index_update_method="BATCH_UPDATE",
    )
    print(f"✅ 필터링 인덱스 생성 완료: {faq_filtered_index.resource_name}")
    return faq_filtered_index


def deploy_filtered_index(faq_filtered_index: aiplatform.MatchingEngineIndex) -> None:
    print("[2/2] 기존 엔드포인트에 필터링 인덱스 배포 중...")

    # 기존 엔드포인트 재사용
    endpoint = aiplatform.MatchingEngineIndexEndpoint(
        index_endpoint_name=INDEX_ENDPOINT_ID
    )
    endpoint.deploy_index(
        index=faq_filtered_index,
        deployed_index_id=FILTERED_DEPLOYED_INDEX_ID,  # 기존과 다른 ID
        min_replica_count=1,
    )
    print(f"✅ 배포 완료 - Deployed Index ID: {FILTERED_DEPLOYED_INDEX_ID}")
    print(f"\n📌 config.py의 FILTERED_INDEX_ID를 아래 값으로 업데이트하세요:")
    print(f"   {faq_filtered_index.resource_name.split('/')[-1]}")


def run():
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    faq_filtered_index = create_filtered_index()
    deploy_filtered_index(faq_filtered_index)

    print("\n✅ 필터링 프로비저닝 완료. 다음 단계: step3_filtered_search.py 실행")


if __name__ == "__main__":
    run()
