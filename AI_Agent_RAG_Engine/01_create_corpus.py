
from vertexai import rag
import vertexai

PROJECT_ID = "vertexailab-495605"
LOCATION = "asia-northeast3"

vertexai.init(project=PROJECT_ID, location=LOCATION)

backend_config = rag.RagVectorDbConfig(
    rag_embedding_model_config=rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model= "publishers/google/models/text-multilingual-embedding-002"
        )
    )
)

corpus = rag.create_corpus(
    display_name="WS_Corpus",
    description="테스트",
    backend_config=backend_config
)