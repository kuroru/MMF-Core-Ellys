"""
$ python create_openapi.py
→ openapi.json 파일이 생성됩니다.
"""
import json, pathlib, importlib
app = importlib.import_module("api.main").app
pathlib.Path("openapi.json").write_text(
    json.dumps(app.openapi(), indent=2, ensure_ascii=False)
)
print("✅ openapi.json 생성 완료")
