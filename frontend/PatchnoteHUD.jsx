import React, { useState } from "react";

export default function PatchnoteHUD() {
  const [keyword, setKeyword] = useState("");
  const [result, setResult] = useState(null);

  const search = async () => {
    if (!keyword) return;
    const res = await fetch(
      `http://localhost:8080/api/verify_event?type=patchnote&keyword=${encodeURIComponent(keyword)}`
    );
    const data = await res.json();
    setResult(data);
  };

  const restorePolicy = async () => {
    const res = await fetch("http://localhost:8080/api/restore_policy", { method: "POST" });
    const data = await res.json();
    alert(data.message);
  };

  return (
    <div className="p-6 bg-black text-white min-h-screen">
      <h2 className="text-2xl mb-4 font-bold">MMF 패치노트 검증 HUD</h2>
      <input
        className="border px-3 py-1 text-black rounded mr-2"
        value={keyword}
        onChange={e => setKeyword(e.target.value)}
        placeholder="예: 시그니처 보상"
      />
      <button
        onClick={search}
        className="bg-blue-500 text-white px-4 py-1 rounded"
      >
        검증
      </button>
      {result && (
        <div className="mt-6">
          {result.found ? (
            <div className="bg-green-700 text-white p-4 rounded-xl">
              ✅ 공식 패치노트에 기록됨
              <pre className="whitespace-pre-wrap">{JSON.stringify(result.matches, null, 2)}</pre>
            </div>
          ) : (
            <div className="bg-red-700 text-white p-4 rounded-xl">
              ⚠️ 공식 패치노트에 기록 없음! 관리자 확인 필요
              <div>{result.message}</div>
              <button
                onClick={restorePolicy}
                className="bg-yellow-500 px-3 py-1 mt-4 rounded text-black font-bold"
              >
                관리자 승인 요청 / 정책 복원
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
