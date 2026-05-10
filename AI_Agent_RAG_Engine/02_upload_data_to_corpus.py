from vertexai import rag
import vertexai

import glob

corpus_name = 'projects/vertexailab-495605/locations/asia-northeast3/ragCorpora/6917529027641081856'
file_paths = glob.glob('./datas/*')


transformation_config = rag.TransformationConfig(
    chunking_config=rag.ChunkingConfig(
        chunk_size=512,
        chunk_overlap=100,
    )
)

rag_files = []

for file_path in file_paths:
    print(f"업로드 중: {file_path}")
    rag_file = rag.upload_file(
        corpus_name=corpus_name,
        path=file_path,
        transformation_config=transformation_config,
    )
    rag_files.append(rag_file)
    print(f"✅ 완료: {rag_file.name}")

print(f"\n총 {len(rag_files)}개 파일 업로드 완료")


