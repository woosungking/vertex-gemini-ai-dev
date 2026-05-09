"""
Vertex AI Search Data Store 생성 + GCS에서 PDF 가져오기
콘솔 UI 대신 Python API로 직접 처리
"""

from google.cloud import discoveryengine_v1 as discoveryengine
from google.api_core.client_options import ClientOptions

PROJECT_ID = "vertexailab-495605"
LOCATION = "global"
DATA_STORE_ID = "nexttech-manuals-datastore"
GCS_URI = "gs://nexttech-manuals-bucket/manuals/"

# 파일 각각 지정
GCS_URIS = [
    "gs://nexttech-manuals-bucket/manuals/NT-S100_Smart_Speaker_Manual.pdf",
    "gs://nexttech-manuals-bucket/manuals/NT-W200_SmartWatch_Manual.pdf",
    "gs://nexttech-manuals-bucket/manuals/NT-R300_Robot_Vacuum_Manual.pdf",
    "gs://nexttech-manuals-bucket/manuals/NT-C400_Security_Camera_Manual.pdf",
]

# 클라이언트 초기화
client_options = ClientOptions(api_endpoint=f"{LOCATION}-discoveryengine.googleapis.com")
ds_client = discoveryengine.DataStoreServiceClient(client_options=client_options)
doc_client = discoveryengine.DocumentServiceClient(client_options=client_options)

parent = f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection"
data_store_name = f"{parent}/dataStores/{DATA_STORE_ID}"


# ============================================================
# STEP 1. Data Store 생성
# ============================================================
def create_data_store():
    print("Data Store 생성 중...")
    try:
        data_store = discoveryengine.DataStore(
            display_name="NextTech Product Manuals",
            industry_vertical=discoveryengine.IndustryVertical.GENERIC,
            content_config=discoveryengine.DataStore.ContentConfig.CONTENT_REQUIRED,
        )
        operation = ds_client.create_data_store(
            parent=parent,
            data_store=data_store,
            data_store_id=DATA_STORE_ID,
        )
        result = operation.result()
        print(f"✅ Data Store 생성 완료: {result.name}")
        return True
    except Exception as e:
        if "already exists" in str(e).lower():
            print(f"✅ Data Store 이미 존재: {data_store_name}")
            return True
        print(f"❌ 생성 실패: {e}")
        return False


# ============================================================
# STEP 2. GCS에서 문서 가져오기
# ============================================================
def import_documents():
    print("\nGCS에서 문서 가져오는 중...")
    try:
        gcs_source = discoveryengine.GcsSource(
            input_uris=GCS_URIS,
            data_schema="content",
        )
        request = discoveryengine.ImportDocumentsRequest(
            parent=f"{data_store_name}/branches/default_branch",
            gcs_source=gcs_source,
            reconciliation_mode=discoveryengine.ImportDocumentsRequest.ReconciliationMode.INCREMENTAL,
        )
        operation = doc_client.import_documents(request=request)
        print("가져오기 진행 중... (완료까지 수 분 소요)")
        result = operation.result()
        print(f"✅ 가져오기 완료")
        print(f"   성공: {result.success_count}건")
        print(f"   실패: {result.failure_count}건")
        return True
    except Exception as e:
        print(f"❌ 가져오기 실패: {e}")
        return False


if __name__ == "__main__":
    if create_data_store():
        import_documents()
    print(f"\n📌 Data Store ID: {DATA_STORE_ID}")
    print(f"   콘솔 확인: https://console.cloud.google.com/gen-app-builder/data-stores?project={PROJECT_ID}")
