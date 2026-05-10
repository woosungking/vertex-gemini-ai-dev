from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project='vertexailab-495605', location='us-central1')

corpus_name = 'projects/vertexailab-495605/locations/asia-northeast3/ragCorpora/6917529027641081856'

rag_retrieval_tool = [
    types.Tool( # 03_ .py 에서 했던 리트리발 로직
        retrieval=types.Retrieval(
            vertex_rag_store=types.VertexRagStore(
                rag_resources=[
                    types.VertexRagStoreRagResource(
                        rag_corpus=corpus_name
                    )
                ],
                rag_retrieval_config=types.RagRetrievalConfig(
                    top_k=3,
                    filter=types.RagRetrievalConfigFilter(
                        vector_distance_threshold=0.5
                    )
                )
            )
        )
    )
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="전산직군은 어떤 전형으로 채용이 이루어지지?",
    config=types.GenerateContentConfig(
        tools=rag_retrieval_tool,
    )
)

print(response.text)
