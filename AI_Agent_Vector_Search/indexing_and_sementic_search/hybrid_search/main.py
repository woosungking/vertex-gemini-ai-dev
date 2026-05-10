"""
하이브리드 검색 실행 진입점

실행: python hybrid_search/main.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from AI_Agent_Vector_Search.indexing_and_sementic_search.faq_filtered_add import faq_data_filtered
from AI_Agent_Vector_Search.indexing_and_sementic_search.hybrid_search.embeddings import fit_tfidf
from AI_Agent_Vector_Search.indexing_and_sementic_search.hybrid_search.search import execute_hybrid_search

# FAQ ID → 원문 텍스트 조회용
FAQ_MAP = {item["id"]: item["text"] for item in faq_data_filtered}

# TF-IDF 학습 (FAQ 전체 텍스트로)
corpus = [item["text"] for item in faq_data_filtered]
fit_tfidf(corpus)


def run(query_text: str, category: str) -> None:
    print(f"\n검색어: '{query_text}' [카테고리: {category}]")
    print("-" * 60)

    response = execute_hybrid_search(query_text, category)

    if not response or not response[0]:
        print("검색 결과가 없습니다.")
        return

    for rank, neighbor in enumerate(response[0], start=1):
        text = FAQ_MAP.get(neighbor.id, "(텍스트 없음)")
        rrf_score = f"{neighbor.distance:.4f}"
        sparse_dist = (
            f"{neighbor.sparse_distance:.4f}"
            if hasattr(neighbor, "sparse_distance") and neighbor.sparse_distance is not None
            else "N/A"
        )
        print(f"[{rank}위] ID: {neighbor.id} | RRF 점수: {rrf_score} | 희소 점수: {sparse_dist}")
        print(f"      {text}\n")


if __name__ == "__main__":
    QUERY = "결제 취소했는데 환불 언제 돼?"
    CATEGORY = "payment"
    run(QUERY, CATEGORY)
