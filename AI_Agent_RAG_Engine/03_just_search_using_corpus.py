from vertexai import rag
import vertexai

vertexai.init(project="vertexailab-495605", location="asia-northeast3")

corpus_name = 'projects/vertexailab-495605/locations/asia-northeast3/ragCorpora/6917529027641081856'

rag_resources = [
    rag.RagResource(
        rag_corpus=corpus_name
    )
]

rag_retrieval_config = rag.RagRetrievalConfig(
    top_k=3,
    filter=rag.Filter(vector_distance_threshold=0.5)
)

response = rag.retrieval_query(
    rag_resources=rag_resources,
    text="전산직군은 어떤 전형으로 채용이 이루어 지지 ?",
    rag_retrieval_config=rag_retrieval_config
)

print(f"검색어: '전산직군은 어떤 전형으로 채용이 이루어 지지 ?'\n")
for i, ctx in enumerate(response.contexts.contexts, start=1):
    print(f"[{i}위] 유사도: {ctx.score:.4f}")
    print(f"      {ctx.text.strip()[:300]}")
    print()
