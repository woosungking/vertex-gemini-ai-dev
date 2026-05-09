"""
카테고리 필터링 버전 인덱싱
  - faq_filtered_add.py의 faq_data_filtered 사용 (category 필드 포함)
  - restricts 필드를 추가해서 JSONL 저장
  - GCS의 별도 경로(Vector_Search/FAQ_filtered)에 업로드
  - 기존 인덱스(Vector_Search/FAQ)와 충돌 없음
"""

import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from google import genai
from google.genai.types import EmbedContentConfig
from google.cloud import storage

from config import (
    PROJECT_ID, LOCATION,
    EMBEDDING_MODEL, EMBEDDING_DIM,
    GCS_BUCKET_NAME, GCS_FILTERED_INPUT_URI,
)
from faq_filtered_add import faq_data_filtered

EMBEDDINGS_FILE = "faq_filtered_embeddings.json"


def get_embedding_vector(
    client: genai.Client,
    texts: List[str],
    task_type: str,
) -> List[List[float]]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=texts,
        config=EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=EMBEDDING_DIM,
        ),
    )
    return [emb.values for emb in response.embeddings]


def upload_to_gcs(local_file: str) -> None:
    gcs_client = storage.Client(project=PROJECT_ID)
    bucket = gcs_client.lookup_bucket(GCS_BUCKET_NAME)
    if not bucket:
        print(f"버킷 생성 중: gs://{GCS_BUCKET_NAME} (리전: {LOCATION})")
        bucket = gcs_client.create_bucket(GCS_BUCKET_NAME, location=LOCATION)
        print(f"✅ 버킷 생성 완료")

    # GCS_FILTERED_INPUT_URI 경로에 업로드 (기존과 다른 경로)
    prefix = GCS_FILTERED_INPUT_URI.replace(f"gs://{GCS_BUCKET_NAME}/", "")
    blob_name = f"{prefix}/{os.path.basename(local_file)}"
    bucket.blob(blob_name).upload_from_filename(local_file)
    print(f"✅ GCS 업로드 완료: gs://{GCS_BUCKET_NAME}/{blob_name}")


def run():
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

    # 1. 벡터화
    print(f"FAQ 데이터 {len(faq_data_filtered)}건 벡터화 중...")
    texts = [item["text"] for item in faq_data_filtered]
    embeddings = get_embedding_vector(client, texts, "RETRIEVAL_DOCUMENT")

    # 2. restricts 포함해서 로컬 저장
    vector_datapoints = [
        {
            "id": item["id"],
            "embedding": emb,
            "restricts": [{"namespace": "category", "allow": [item["category"]]}],
        }
        for item, emb in zip(faq_data_filtered, embeddings)
    ]
    with open(EMBEDDINGS_FILE, "w") as f:
        for dp in vector_datapoints:
            f.write(json.dumps(dp) + "\n")
    print(f"✅ 로컬 저장 완료: {EMBEDDINGS_FILE} ({len(vector_datapoints)}건)")

    # 3. GCS 업로드 (Vector_Search/FAQ_filtered/ 경로)
    print("GCS 업로드 중...")
    upload_to_gcs(EMBEDDINGS_FILE)

    print("\n✅ 필터링 인덱싱 완료. 다음 단계: filtered_step2_provisioning.py 실행")


if __name__ == "__main__":
    run()
