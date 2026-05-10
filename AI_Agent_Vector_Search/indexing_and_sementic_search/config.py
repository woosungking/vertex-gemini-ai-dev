# ============================================================
# 공통 설정
# ============================================================

PROJECT_ID = "vertexailab-495605"
LOCATION = "asia-northeast3"

# 임베딩 모델
EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIM = 768

# Vector Search 인덱스
INDEX_DISPLAY_NAME = "faq_index"
INDEX_ID = "1889299626100523008"
DEPLOYED_INDEX_ID = "faq_index_deployed"

# Vector Search 필터링 인덱스
FILTERED_INDEX_DISPLAY_NAME = "faq_filtered_index"
FILTERED_INDEX_ID = ""  # 필터링 인덱스 프로비저닝 후 채워넣기
FILTERED_DEPLOYED_INDEX_ID = "faq_filtered_index_deployed"

# GCS 경로 (faq_embeddings.json 업로드 위치)
GCS_BUCKET_NAME = "vertexai-faq-search-2026"
GCS_INPUT_URI = f"gs://{GCS_BUCKETs_NAME}/Vector_Search/FAQ"
GCS_FILTERED_INPUT_URI = f"gs://{GCS_BUCKET_NAME}/Vector_Search/FAQ_filtered"

# 엔드포인트 ID (프로비저닝 후 콘솔에서 확인해서 채워넣기)
INDEX_ENDPOINT_ID = "243132807226851328"

# 로컬 임베딩 파일 경로
EMBEDDINGS_FILE = "faq_embeddings.json"
