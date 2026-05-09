"""
STEP 1. 인덱싱
  - FAQ 텍스트를 벡터로 변환
  - faq_embeddings.jsonl 로컬 저장
  - GCS 버킷 없으면 자동 생성 후 업로드

데이터가 바뀔 때마다 재실행하면 됩니다.
"""

import json
import os
from typing import List

from google import genai
from google.genai.types import EmbedContentConfig
from google.cloud import storage

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    PROJECT_ID, LOCATION,
    EMBEDDING_MODEL, EMBEDDING_DIM,
    EMBEDDINGS_FILE, GCS_BUCKET_NAME, GCS_INPUT_URI,
)
from faq import faq_data_raw


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
    """버킷 없으면 생성 후 GCS에 업로드"""
    gcs_client = storage.Client(project=PROJECT_ID)

    # 버킷 없으면 생성
    bucket = gcs_client.lookup_bucket(GCS_BUCKET_NAME)
    if not bucket:
        print(f"버킷 생성 중: gs://{GCS_BUCKET_NAME} (리전: {LOCATION})")
        bucket = gcs_client.create_bucket(GCS_BUCKET_NAME, location=LOCATION)
        print(f"✅ 버킷 생성 완료")
    
    # 업로드
    prefix = GCS_INPUT_URI.replace(f"gs://{GCS_BUCKET_NAME}/", "")
    blob_name = f"{prefix}/{os.path.basename(local_file)}"
    bucket.blob(blob_name).upload_from_filename(local_file)
    print(f"✅ GCS 업로드 완료: gs://{GCS_BUCKET_NAME}/{blob_name}")


def run():
    client = genai.Client(vertexai=True, project=PROJECT_ID, location="global")

    # 1. 벡터화
    print(f"FAQ 데이터 {len(faq_data_raw)}건 벡터화 중...")
    texts = [item["text"] for item in faq_data_raw]
    embeddings = get_embedding_vector(client, texts, "RETRIEVAL_DOCUMENT")

    # 2. 로컬 저장
    vector_datapoints = [
        {"id": item["id"], "embedding": emb}
        for item, emb in zip(faq_data_raw, embeddings)
    ]
    with open(EMBEDDINGS_FILE, "w") as f:
        for dp in vector_datapoints:
            f.write(json.dumps(dp) + "\n")
    print(f"✅ 로컬 저장 완료: {EMBEDDINGS_FILE} ({len(vector_datapoints)}건)")

    # 3. GCS 업로드
    print("GCS 업로드 중...")
    upload_to_gcs(EMBEDDINGS_FILE)

    print("\n✅ 인덱싱 완료. 다음 단계: 2번(프로비저닝) 실행")
