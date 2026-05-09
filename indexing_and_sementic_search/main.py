"""
FAQ Vector Search 파이프라인

실행: python main.py

정규 절차:
  1. 인덱싱     - FAQ 텍스트 벡터화 → GCS 업로드
  2. 프로비저닝 - 인덱스/엔드포인트 생성 및 배포 (최초 1회)
  3. 검색       - 질문 입력 → 유사 FAQ 검색

비정규 (데이터 변경 시):
  r. 재인덱싱   - GCS 데이터로 인덱스 재구축
"""

from importlib import import_module

_01 = import_module("semantic.01_embed_and_upload")
_02 = import_module("semantic.02_create_index_and_deploy")
_03 = import_module("semantic.03_search")
_rebuild = import_module("semantic.rebuild_index")

MENU = """
========================================
  FAQ Vector Search 파이프라인
========================================
  1. 인덱싱     (FAQ 벡터화 + GCS 업로드)
  2. 프로비저닝 (인덱스/엔드포인트 생성)
  3. 검색       (유사 FAQ 검색)
  r. 재인덱싱   (데이터 변경 시 인덱스 재구축)
  0. 종료
========================================
선택: """


def main():
    while True:
        choice = input(MENU).strip()

        if choice == "1":
            _01.run()
        elif choice == "2":
            _02.run()
        elif choice == "3":
            _03.run()
        elif choice == "r":
            _rebuild.run()
        elif choice == "0":
            print("종료합니다.")
            break
        else:
            print("1, 2, 3, r, 0 중에서 선택해주세요.")


if __name__ == "__main__":
    main()
