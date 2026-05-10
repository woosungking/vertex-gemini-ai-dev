"""
FAQ Vector Search 파이프라인

실행: python main.py

메뉴:
  1. 프로비저닝  - Vector Search 인덱스/엔드포인트 생성 및 배포 (최초 1회)
  2. 인덱싱     - FAQ 텍스트 벡터화 → faq_embeddings.json 저장 (데이터 변경 시)
  3. 검색       - 질문 입력 → 유사 FAQ 검색
  0. 종료
"""

from AI_Agent_Vector_Search.indexing_and_sementic_search.semantic import step3_sementic_search
from AI_Agent_Vector_Search.indexing_and_sementic_search.semantic import step1_provisioning, step2_indexing

MENU = """
========================================
  FAQ Vector Search 파이프라인
========================================
  1. 프로비저닝  (인덱스/엔드포인트 생성)
  2. 인덱싱      (FAQ 벡터화 및 저장)
  3. 검색        (유사 FAQ 검색)
  0. 종료
========================================
선택: """


def main():
    while True:
        choice = input(MENU).strip()

        if choice == "1":
            step1_provisioning.run()
        elif choice == "2":
            step2_indexing.run()
        elif choice == "3":
            step3_sementic_search.run()
        elif choice == "0":
            print("종료합니다.")
            break
        else:
            print("1, 2, 3, 0 중에서 선택해주세요.")


if __name__ == "__main__":
    main()
