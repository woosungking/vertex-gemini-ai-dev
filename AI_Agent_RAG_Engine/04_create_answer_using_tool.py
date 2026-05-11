from google import genai
from google.genai import types

client = genai.Client(vertexai=True, project='vertexailab-495605', location='us-central1')

corpus_name = 'projects/vertexailab-495605/locations/asia-northeast3/ragCorpora/6917529027641081856'
vector_search_corpus_name = 'projects/vertexailab-495605/locations/asia-northeast3/ragCorpora/1152921504606846976'

rag_retrieval_tool = [
    types.Tool( # 03_ .py 에서 했던 리트리발 로직
        retrieval=types.Retrieval(
            vertex_rag_store=types.VertexRagStore(
                rag_resources=[
                    types.VertexRagStoreRagResource(
                        rag_corpus=vector_search_corpus_name
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
    contents="전산직군 채용 일정 정리",
    config=types.GenerateContentConfig(
        tools=rag_retrieval_tool,
        system_instruction="너는 인천대학교 채용담당관이야 제공된 문서(도구)를 검색할 때 연도(2023년, 2025년 등)는 무시해. 문서의 텍스트가 '전 산', '필기+실기'처럼 표 형태로 깨져 있더라도, 눈치껏 조합해서 '전산직군은 서류 전형, 필기 및 실기 전형을 진행합니다'처럼 자연스러운 문장으로 대답해."
    )
)

print(response.text)
