"use client";

import { useState, type FormEvent } from "react";

import { PageIntro } from "@/components/common/page-intro";
import { ScoreTrace } from "@/components/scoring/trace";
import { Card } from "@/components/ui/card";
import { score, type ScoreResponse } from "@/lib/api";

export default function ScoringPage() {
  const [amount, setAmount] = useState("");
  const [result, setResult] = useState<ScoreResponse>();
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");
    setResult(undefined);
    try {
      setResult(await score({ feature_schema_id: "sample-v1", transaction: { amount: Number(amount) }, mode: "stub" }));
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : "Scoring is unavailable.");
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <PageIntro title="Transaction scoring" description="Use a synthetic amount to observe the two-stage routing policy." />
      <Card>
        <form onSubmit={submit}>
          <label>Sample amount in INR
            <input required min="0" step="0.01" type="number" value={amount}
              onChange={event => setAmount(event.target.value)} />
          </label>
          <div className="actions">
            <button className="primary" type="submit" disabled={busy}>Score transaction</button>
            <button className="secondary" type="button" onClick={() => setAmount("5")}>Pick a sample</button>
          </div>
        </form>
      </Card>
      <Card aria-live="polite">
        {busy ? <p role="status">Scoring sample…</p> : error ? <p role="alert">{error}</p>
          : result ? <ScoreTrace result={result} /> : <p>Submit a synthetic transaction to see its scoring trace.</p>}
      </Card>
    </>
  );
}
