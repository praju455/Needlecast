import type { paths } from "./types/api";

type Gets = { [P in keyof paths]: paths[P] extends { get: { responses: { 200: unknown } } } ? P : never }[keyof paths];
export type ReadResponse<P extends Gets> =
  paths[P]["get"]["responses"][200]["content"]["application/json"];
export type ScoreRequest =
  paths["/api/score"]["post"]["requestBody"]["content"]["application/json"];
export type ScoreResponse =
  paths["/api/score"]["post"]["responses"][200]["content"]["application/json"];

export class ApiError extends Error {
  constructor(message: string, readonly code: string, readonly requestId?: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  try {
    const response = await fetch(path, { ...init, signal: AbortSignal.timeout(6000) });
    if (!response.ok) {
      const detail = await response.json().catch(() => ({}));
      throw new ApiError(
        detail.message ?? "The service did not return the requested data.",
        detail.code ?? "request_failed",
        detail.request_id ?? response.headers.get("x-request-id") ?? undefined,
      );
    }
    return await response.json() as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;
    throw new ApiError("Could not reach the API. Check that the backend is running.", "unavailable");
  }
}

export function readApi<P extends Gets>(path: P) {
  return request<ReadResponse<P>>(path);
}

export function score(payload: ScoreRequest) {
  return request<ScoreResponse>("/api/score", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
  });
}
