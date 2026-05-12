import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types
from seq_n_parallel_agent import root_agent  # 에이전트 파일에서 import

# Vertex AI 설정
os.environ["GOOGLE_CLOUD_PROJECT"] = "vertexailab-495605"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

async def main():
    # 1. 세션(대화방)과 러너(실행기) 준비
    session_service = InMemorySessionService()
    
    # 핵심! Runner에 우리가 만든 최종 파이프라인(root_agent)을 통째로 넣습니다.
    runner = Runner(
        agent=root_agent, 
        app_name="research_app",
        session_service=session_service,
    )
    
    session = await session_service.create_session(
        app_name="research_app",
        user_id="user_001",
    )
    
    print("🚀 연구 조사를 시작합니다...")
    
    # 2. 실행 명령 하달! ("자, 계획대로 실행해!")
    response_text = ""
    async for event in runner.run_async(
        user_id="user_001",
        session_id=session.id,
        new_message=genai_types.Content(
            role="user",
            parts=[genai_types.Part(text="지속 가능한 기술 트렌드 조사 파이프라인 가동해줘.")]
        )
    ):
        # 3. 모든 에이전트의 작업이 끝나고 최종 보고서가 나오면 출력
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    response_text = part.text
                    
    print("\n[최종 병합 보고서]")
    print(response_text)

# 프로그램 실행
if __name__ == "__main__":
    asyncio.run(main())