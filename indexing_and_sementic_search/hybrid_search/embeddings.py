"""
Dense(의미) + Sparse(키워드) 임베딩 생성
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Any
from google import genai
from google.genai.types import EmbedContentConfig
from sklearn.feature_extraction.text import TfidfVectorizer

from config import PROJECT_ID, LOCATION, EMBEDDING_MODEL, EMBEDDING_DIM

genai_client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# TF-IDF 벡터라이저 (fit은 외부에서 호출)
vectorizer = TfidfVectorizer()


def fit_tfidf(corpus: List[str]) -> None:
    """FAQ 텍스트로 TF-IDF 사전 학습"""
    vectorizer.fit_transform(corpus)


def get_dense_embedding(text: str) -> List[float]:
    """Gemini 모델로 의미 기반 밀집 벡터 생성"""
    response = genai_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[text],
        config=EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=EMBEDDING_DIM,
        ),
    )
    return response.embeddings[0].values


def get_sparse_embedding(text: str) -> Dict[str, List[Any]]:
    """TF-IDF로 키워드 기반 희소 벡터 생성"""
    tfidf_vector = vectorizer.transform([text])
    values = []
    dims = []
    for i, tfidf_value in enumerate(tfidf_vector.data):
        values.append(float(tfidf_value))
        dims.append(int(tfidf_vector.indices[i]))
    return {"values": values, "dimensions": dims}
