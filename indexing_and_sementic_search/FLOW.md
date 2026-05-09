# FAQ Vector Search 순서도

## 최초 구축

```mermaid
flowchart TD
    A([시작]) --> B
    B[faq.py 텍스트 로드] --> C
    C[gemini-embedding-001로 벡터화] --> D
    D[faq_embeddings.jsonl 로컬 저장] --> E

    E --> GCS[(GCS\ngs://버킷/Vector_Search/FAQ/)]

    GCS --> F
    F[Vector Search 인덱스 생성] --> G
    G[엔드포인트 생성] --> H
    H[엔드포인트에 인덱스 배포] --> I
    I[config.py INDEX_ENDPOINT_ID 업데이트] --> J

    J[사용자 질문 입력] --> K
    K[질문 벡터화] --> L
    L[Vector Search 유사도 검색] --> M
    M[ID 반환] --> N
    N[FAQ_MAP으로 원문 조회] --> O([결과 출력])

    B:::step1
    C:::step1
    D:::step1
    E:::step1
    F:::step2
    G:::step2
    H:::step2
    I:::step2
    J:::step3
    K:::step3
    L:::step3
    M:::step3
    N:::step3
    O:::step3

    classDef step1 fill:#1a3a5c,stroke:#4a9eff,color:#fff
    classDef step2 fill:#1a3a2c,stroke:#4aff9e,color:#fff
    classDef step3 fill:#3a1a3a,stroke:#ff4aff,color:#fff
```

---

## 데이터 변경 시

```mermaid
flowchart TD
    A([faq.py 수정]) --> B

    subgraph STEP1["① 인덱싱 재실행"]
        B[텍스트 재벡터화] --> C[faq_embeddings.jsonl 갱신]
        C --> D[GCS 덮어쓰기]
    end

    D --> E

    subgraph UTIL["r. 재인덱싱 (util_reindex.py)"]
        E[GCS 데이터로\n인덱스 재구축]
        E --> F[콘솔에서 일집수 확인\n데이터 수와 일치할 때까지 대기]
    end

    F --> G([검색 가능])

    style STEP1 fill:#1a3a5c,stroke:#4a9eff,color:#fff
    style UTIL fill:#3a2a1a,stroke:#ffaa4a,color:#fff
```

---

## ⚠️ 주의사항

| 상황 | 증상 | 해결 |
|------|------|------|
| 프로비저닝을 인덱싱보다 먼저 실행 | 빈 인덱스 생성, 검색 결과 없음 | 인덱싱 후 `r. 재인덱싱` 실행 |
| GCS 버킷 리전 불일치 | `FailedPrecondition 400` 에러 | 버킷을 `asia-northeast3`으로 새로 생성 |
| 재인덱싱 직후 바로 검색 | 빈 결과 반환 | 콘솔에서 일집수 확인 후 검색 |
| INDEX_ENDPOINT_ID 미업데이트 | `NotFound 404` 에러 | 프로비저닝 후 출력된 ID로 config.py 수정 |
