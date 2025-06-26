// frontend/src/api/chat.ts

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
}

/**
 * バックエンドの /api/chat エンドポイントへ質問を送信し、
 * RAG 処理のレスポンス文字列を返します。
 *
 * 環境変数 VITE_API_BASE_URL をベース URL として使用します。
 */
export async function sendQuery(question: string): Promise<string> {
  const res = await fetch(
    // @ts-ignore
    import.meta.env.VITE_API_BASE_URL + '/api/chat',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question } as ChatRequest),
    }
  );
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  const data = (await res.json()) as ChatResponse;
  return data.answer;
}
