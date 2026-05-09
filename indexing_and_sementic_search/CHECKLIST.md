# FAQ Vector Search 운영 체크리스트

실제 겪은 문제들을 기반으로 작성

---

## 최초 구축 순서 (반드시 이 순서대로)

- [ ] 1. `python main.py` → **2번 인덱싱** 먼저 실행 (벡터화 + GCS 업로드)
- [ ] 2. GCS 업로드 완료 확인
- [ ] 3. **1번 프로비저닝** 실행 (버킷/인덱스/엔드포인트 생성)
- [ ] 4. 출력된 `INDEX_ENDPOINT_ID` 값을 `config.py`에 업데이트
- [ ] 5. 콘솔에서 인덱스 상태 "준비됨" + 일집수 100 확인 후 검색

> ⚠️ 인덱싱보다 프로비저닝을 먼저 하면 빈 인덱스가 생성됨
> → 이 경우 4번(인덱스 업데이트) 실행 후 반영될 때까지 대기 필요

---

## GCS 버킷 생성 시

- [ ] 리전을 **asia-northeast3 (서울)** 로 설정
- [ ] Vector Search 리전과 반드시 동일해야 함

> ⚠️ 버킷 리전이 다르면 인덱스 생성 시 `FailedPrecondition 400` 에러 발생
> → 버킷 리전은 생성 후 변경 불가, 새로 만들어야 함

---

## config.py 설정 확인

- [ ] `PROJECT_ID` 올바른 프로젝트 ID인지 확인
- [ ] `LOCATION` = `asia-northeast3`
- [ ] `GCS_BUCKET_NAME` 실제 존재하는 버킷 이름인지 확인
- [ ] `INDEX_ENDPOINT_ID` 프로비저닝 후 출력된 값으로 업데이트했는지 확인
- [ ] `INDEX_ID` 프로비저닝 후 출력된 값으로 업데이트했는지 확인

> ⚠️ INDEX_ENDPOINT_ID가 이전 값이면 `NotFound 404` 에러 발생

---

## 인덱스 업데이트(4번) 후 검색 시

- [ ] SDK가 "업데이트 완료" 메시지를 출력해도 바로 검색하지 말 것
- [ ] GCP 콘솔 → Vector Search → 인덱스 → 일집수(인덱싱된 벡터 개수)가 FAQ 데이터 수(100)와 일치할 때까지 대기
- [ ] 일집수 확인 후 검색 실행

> ⚠️ `update_embeddings()`는 비동기로 동작
> → SDK 완료 메시지 ≠ 실제 반영 완료
> → 반영 전 검색하면 `response []` 빈 결과 반환

---

## 검색 결과가 없을 때 점검 순서

1. 콘솔에서 인덱스 일집수 확인 (0이면 아직 반영 중)
2. `config.py`의 `INDEX_ENDPOINT_ID` 값이 맞는지 확인
3. `config.py`의 `DEPLOYED_INDEX_ID` = `faq_index_deployed` 인지 확인
4. 인덱스 상태가 "준비됨"인지 확인
5. 위 모두 정상이면 잠시 대기 후 재시도

---

## SDK 관련

- [ ] `google-genai` 패키지 설치 확인 (`pip install google-genai`)
- [ ] `google-cloud-aiplatform` 패키지 설치 확인
- [ ] `google-cloud-storage` 패키지 설치 확인
- [ ] `import vertexai` + `vertexai.init()` 은 이 프로젝트에서 불필요 (삭제해도 됨)

> ℹ️ `vertexai` SDK의 Generative AI 모듈은 2026년 6월 24일 이후 제거됨
> → `google-genai` SDK로 대체
> → `aiplatform` (Vector Search 인프라)은 계속 유지
