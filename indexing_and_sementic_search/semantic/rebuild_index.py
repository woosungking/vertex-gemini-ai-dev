"""
STEP 4. 인덱스 업데이트
  - GCS에 올라간 faq_embeddings.json으로 인덱스 재구축
  - 처음 프로비저닝 후 데이터가 비어있을 때 실행
  - FAQ 데이터 변경 후 재인덱싱 시에도 실행

완료까지 10~20분 소요됩니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from google.cloud import aiplatform
from config import PROJECT_ID, LOCATION, INDEX_ID, GCS_INPUT_URI


def run():
    aiplatform.init(project=PROJECT_ID, location=LOCATION)

    print(f"인덱스 업데이트 중... (10~20분 소요)")
    print(f"데이터 소스: {GCS_INPUT_URI}")

    faq_index = aiplatform.MatchingEngineIndex(
        index_name=INDEX_ID
    )
    faq_index.update_embeddings(
        contents_delta_uri=GCS_INPUT_URI,
        is_complete_overwrite=True,
    )

    print("✅ 인덱스 업데이트 완료. 이제 3번(검색) 실행 가능합니다.")
