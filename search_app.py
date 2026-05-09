"""
NextTech 제품 매뉴얼 검색 데모
실행: python search_app.py
접속: http://localhost:5000
"""

from flask import Flask, request, jsonify, render_template_string
from google.cloud import discoveryengine_v1 as discoveryengine

app = Flask(__name__)

PROJECT_ID = "vertexailab-495605"
LOCATION = "global"
DATA_STORE_ID = "nexttech-manuals-datastore"
SERVING_CONFIG = (
    f"projects/{PROJECT_ID}/locations/{LOCATION}/collections/default_collection"
    f"/dataStores/{DATA_STORE_ID}/servingConfigs/default_config"
)

search_client = discoveryengine.SearchServiceClient()

HTML = """
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8"/>
  <title>NextTech 매뉴얼 검색</title>
  <style>
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family: -apple-system, sans-serif; background:#0f1117; color:#e2e8f0; min-height:100vh; }
    header { padding:20px 40px; border-bottom:1px solid #1e2433; display:flex; align-items:center; gap:10px; }
    .logo { font-size:20px; font-weight:800; background:linear-gradient(135deg,#3b82f6,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    main { max-width:720px; margin:60px auto; padding:0 20px; }
    h1 { font-size:36px; font-weight:800; text-align:center; margin-bottom:8px; }
    h1 span { background:linear-gradient(135deg,#3b82f6,#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .sub { text-align:center; color:#64748b; margin-bottom:40px; }
    .search-box { display:flex; gap:10px; margin-bottom:32px; }
    input { flex:1; padding:14px 18px; background:#1a1f2e; border:1px solid #2d3748; border-radius:10px; color:#e2e8f0; font-size:15px; outline:none; }
    input:focus { border-color:#3b82f6; }
    button { padding:14px 24px; background:linear-gradient(135deg,#3b82f6,#8b5cf6); border:none; border-radius:10px; color:#fff; font-size:15px; font-weight:600; cursor:pointer; }
    button:hover { opacity:0.9; }
    .result { background:#1a1f2e; border:1px solid #1e2433; border-radius:12px; padding:20px; margin-bottom:12px; }
    .result-title { font-weight:700; color:#3b82f6; margin-bottom:8px; font-size:15px; }
    .result-snippet { color:#94a3b8; font-size:14px; line-height:1.6; }
    .loading { text-align:center; color:#64748b; padding:20px; }
    .empty { text-align:center; color:#475569; padding:40px; }
  </style>
</head>
<body>
  <header>
    <span>⚡</span>
    <span class="logo">NextTech</span>
    <span style="font-size:12px;color:#475569;margin-left:8px;">AI 매뉴얼 검색</span>
  </header>
  <main>
    <h1>제품 매뉴얼을<br/><span>AI로 검색</span></h1>
    <p class="sub">NT-S100 · NT-W200 · NT-R300 · NT-C400</p>
    <div class="search-box">
      <input id="q" placeholder="예: 배터리 얼마나 가요? 와이파이 연결 안 돼요" onkeydown="if(event.key==='Enter')search()"/>
      <button onclick="search()">검색</button>
    </div>
    <div id="results"></div>
  </main>
  <script>
    async function search() {
      const q = document.getElementById('q').value.trim();
      if (!q) return;
      const el = document.getElementById('results');
      el.innerHTML = '<p class="loading">검색 중...</p>';
      const res = await fetch('/search?q=' + encodeURIComponent(q));
      const data = await res.json();
      if (!data.results || data.results.length === 0) {
        el.innerHTML = '<p class="empty">검색 결과가 없습니다.</p>';
        return;
      }
      el.innerHTML = data.results.map(r => `
        <div class="result">
          <div class="result-title">${r.title}</div>
          <div class="result-snippet">${r.snippet}</div>
        </div>
      `).join('');
    }
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"results": []})

    try:
        response = search_client.search(
            discoveryengine.SearchRequest(
                serving_config=SERVING_CONFIG,
                query=query,
                page_size=5,
                content_search_spec=discoveryengine.SearchRequest.ContentSearchSpec(
                    snippet_spec=discoveryengine.SearchRequest.ContentSearchSpec.SnippetSpec(
                        return_snippet=True,
                        max_snippet_count=1,
                    )
                ),
            )
        )

        results = []
        for r in response.results:
            data = r.document.derived_struct_data
            title = data.get("title", {}).get("string_value", "제목 없음") if hasattr(data.get("title", ""), "string_value") else str(data.get("title", "제목 없음"))
            snippets = data.get("snippets", [])
            snippet = ""
            if snippets:
                s = snippets[0]
                snippet = s.get("snippet", {}).get("string_value", "") if hasattr(s.get("snippet", ""), "string_value") else str(s.get("snippet", ""))
            results.append({"title": title, "snippet": snippet or "내용을 불러올 수 없습니다."})

        return jsonify({"results": results})

    except Exception as e:
        return jsonify({"error": str(e), "results": []})


if __name__ == "__main__":
    print("서버 시작: http://localhost:5000")
    app.run(debug=True, port=5000)
