import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from google import genai
from google.genai import types

# ==========================================
# 1. 환경 설정 및 클라이언트 초기화 (App Setup)
# ==========================================
PROJECT_ID = "vertexailab-495605"
LOCATION = "us-central1"

# Gemini AI 클라이언트 생성
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

# ==========================================
# 2. MCP 서버 구동 설정 (MCP Server Config)
# ==========================================
# 도커의 ENTRYPOINT/CMD 설정과 같이 서버 프로세스를 어떻게 띄울지 정의합니다.
server_params = StdioServerParameters(
    command="npx",
    args=[
        "-y", 
        "--no-install", # 매번 설치 확인하지 않음
        "@modelcontextprotocol/server-filesystem", 
        "/Users/kimwoosung/Desktop/vertex-gemini-ai-dev"
    ],
    env={"NPM_CONFIG_LOGLEVEL": "silent"}, # npm 관련 로그 완전 차단
)

async def run():
    # ==========================================
    # 3. MCP 통신 연결 및 핸드셰이크 (MCP Connection)
    # ==========================================
    # stdio(표준 입출력)를 통해 외부 프로세스(FileSystem 서버)와 통신 채널을 엽니다.
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # MCP 규격에 따라 서버와 클라이언트가 서로의 기능을 확인(Initialize)합니다.
            await session.initialize()

            # (선택 사항) 서버가 어떤 도구들을 가지고 있는지 목록을 가져와 출력해봅니다.
            tools_list = await session.list_tools()
            print("## [시스템] 연결된 MCP 서버의 도구들을 로드했습니다.")
            for tool in tools_list.tools:
                print(f"  - 발견된 도구: {tool.name}")

            # ==========================================
            # 4. AI 모델 실행 및 서비스 로직 (Application Logic)
            # ==========================================
            # 사용자 질문 정의
            user_prompt = "현재 디렉토리의 파일 목록 보여주고 MCP폴더에 아무 readme.md 파일 하나만드러줘"
            
            # Gemini에게 질문을 던질 때 'MCP 세션' 자체를 도구함에 넣어줍니다.
            # SDK가 내부적으로 MCP 세션의 도구 명세(JSON-RPC)를 추출하여 모델에게 전달합니다.
            response = await client.aio.models.generate_content(
                model="gemini-2.5-flash", # 최신 모델명 사용 권장
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    temperature=0,      # 답변의 일관성을 위해 0으로 설정
                    tools=[session],    # MCP 서버의 모든 기능을 모델에게 부여
                    # automatic_function_calling은 기본적으로 True로 작동합니다.
                ),
            )

            print("\n## [AI 응답]")
            print(response.text)

# 비동기 루프 실행
if __name__ == "__main__":
    asyncio.run(run())