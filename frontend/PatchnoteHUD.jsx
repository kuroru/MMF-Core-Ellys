// 파일: /frontend/PatchnoteHUD.jsx

import React, { useState, useEffect } from "react";

export default function PatchnoteHUD() {
  const [keyword, setKeyword] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [log, setLog] = useState([]);
  const [error, setError] = useState("");

  // 이력 불러오기 (옵션: 백엔드에 /api/event_log 등 추가하면 자동화 가능)
  useEffect(() => {
    // 추후 API 연동 가능: fetch("/api/event_log")
    // 지금은 임시로 sessionStorage 사용 (실전 배포시 교체)
    const prevLog = JSON.parse(sessionStorage.getItem("patchnoteLog") || "[]");
    setLog(prevLog);
  }, []);

  const updateLog = entry => {
    const newLog = [entry, ...log].slice(0, 10);
    setLog(newLog);
    sessionStorage.setItem("patchnoteLog", JSON.stringify(newLog));
  };

  // 검증 API 요청
  const search = async () => {
    setLoading(true);
    setResult(null);
    setError("");
    try {
      const res = await fetch(
        `http://localhost:8080/api/verify_event?type=patchnote&keyword=${encodeURIComponent(
          keyword
        )}`
      );
      const data = await res.json();
      setResult(data);
      updateLog({
        timestamp: new Date().toLocaleString(),
        keyword,
        status: data.found ? "공식 기록 있음" : "경고: 기록 없음",
        message: data.message || "",
      });
    } catch (e) {
      setError("API 요청 실패: 서버 상태/네트워크 확인");
    }
    setLoading(false);
  };

  // 관리자 승인/정책 복원 API 호출
  const restorePolicy = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:8080/api/restore_policy", {
        method: "POST",
      });
      const data = await res.json();
      alert(data.message);
      updateLog({
        timestamp: new Date().toLocaleString(),
        keyword: "[관리자 복원]",
        status: "정책 복원/승인",
        message: data.message,
      });
    } catch (e) {
      setError("정책 복원 요청 실패");
    }
    setLoading(false);
  };

  return (
    <div className="p-8 bg-black min-h-screen text-white">
      <h2 className="text-2xl font-bold mb-4">MMF 패치노트/정책 검증 HUD</h2>
      <div className="mb-4">
        <input
          className="border px-3 py-1 text-black rounded mr-2"
          value={keyword}
          onChange={e => setKeyword(e.target.value)}
          placeholder="예: 시그니처 보상"
          onKeyDown={e => e.key === "Enter" && search()}
        />
        <button
          onClick={search}
          className="bg-blue-500 text-white px-4 py-1 rounded"
          disabled={loading || !keyword}
        >
          {loading ? "검증 중..." : "검증"}
        </button>
      </div>
      {error && (
        <div className="bg-red-800 text-white p-3 rounded mb-2">{error}</div>
      )}
      {result && (
        <div className="mb-6">
          {result.found ? (
            <div className="bg-green-700 text-white p-4 rounded-xl">
              ✅ 공식 패치노트에 기록됨
              <pre className="whitespace-pre-wrap text-white">
                {JSON.stringify(result.matches, null, 2)}
              </pre>
            </div>
          ) : (
            <div className="bg-red-700 text-white p-4 rounded-xl">
              ⚠️ 공식 기록 없음! 관리자 확인 필요
              <div>{result.message}</div>
              <button
                onClick={restorePolicy}
                className="bg-yellow-500 px-3 py-1 mt-4 rounded text-black font-bold"
                disabled={loading}
              >
                관리자 승인 요청 / 정책 복원
              </button>
            </div>
          )}
        </div>
      )}

      {/* 이력 테이블 */}
      <div className="mt-8">
        <h3 className="text-lg font-semibold mb-2">최근 검증/이력</h3>
        <table className="w-full text-left border-collapse bg-gray-800 rounded-xl">
          <thead>
            <tr className="bg-gray-700">
              <th className="px-2 py-1">시간</th>
              <th className="px-2 py-1">키워드</th>
              <th className="px-2 py-1">상태</th>
              <th className="px-2 py-1">비고</th>
            </tr>
          </thead>
          <tbody>
            {log.length === 0 && (
              <tr>
                <td colSpan={4} className="text-center py-2">
                  (이력 없음)
                </td>
              </tr>
            )}
            {log.map((item, i) => (
              <tr key={i} className="border-t border-gray-700">
                <td className="px-2 py-1">{item.timestamp}</td>
                <td className="px-2 py-1">{item.keyword}</td>
                <td className="px-2 py-1">{item.status}</td>
                <td className="px-2 py-1">{item.message}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
