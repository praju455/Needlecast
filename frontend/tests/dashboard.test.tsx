import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PlaceholderBanner } from "@/components/common/placeholder-banner";
import { ScoreTrace } from "@/components/scoring/trace";
import { readApi, score, type ScoreResponse } from "@/lib/api";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

describe("placeholder dashboard", () => {
  it("shows a persistent data notice", () => {
    render(<PlaceholderBanner />);
    expect(screen.getByText("Placeholder data")).toBeTruthy();
  });

  it("marks a bypassed quantum stage as skipped", () => {
    const result = {
      mode: "stub",
      decision: "clear",
      threshold: 0.6,
      final_score: 0.17,
      stages: [{ name: "Quantum re-score", invoked: false, score: null, latency_ms: null, notes: "Bypass" }],
    } as ScoreResponse;
    render(<ScoreTrace result={result} />);
    expect(screen.getByText("Skipped").closest("li")?.dataset.invoked).toBe("false");
  });
});

describe("typed API client", () => {
  it("normalizes safe server errors", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(
      JSON.stringify({ code: "artifact_missing", message: "Generate samples.", request_id: "sample" }),
      { status: 404 },
    )));
    await expect(readApi("/api/datasets")).rejects.toMatchObject({
      code: "artifact_missing", message: "Generate samples.", requestId: "sample",
    });
  });

  it("posts a labelled sample", async () => {
    const fetch = vi.fn().mockResolvedValue(new Response(JSON.stringify({ mode: "stub" })));
    vi.stubGlobal("fetch", fetch);
    await score({ feature_schema_id: "sample-v1", transaction: { amount: 5 }, mode: "stub" });
    expect(fetch).toHaveBeenCalledWith("/api/score", expect.objectContaining({
      method: "POST", body: expect.stringContaining('"mode":"stub"'),
    }));
  });
});
