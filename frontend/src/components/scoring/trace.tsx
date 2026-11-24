import type { ScoreResponse } from "@/lib/api";
import { percent } from "@/lib/format";

export function ScoreTrace({ result }: { result: ScoreResponse }) {
  return (
    <>
      <h2>Scoring trace</h2>
      <p><strong>{result.decision === "review" ? "Send to review" : "Clear"}</strong>
        {" · "}{percent.format(result.final_score)} score and {percent.format(result.threshold)} threshold
      </p>
      <ol className="trace">
        {result.stages.map(stage => (
          <li key={stage.name} data-invoked={stage.invoked}>
            <strong>{stage.name}</strong>{" "}
            <span>{!stage.invoked ? "Skipped" : stage.score == null ? "Unavailable" : percent.format(stage.score)}</span>
            <p className="muted">{stage.notes}</p>
          </li>
        ))}
      </ol>
      <h2>Explanation</h2>
      <p className="muted">Feature contributions and support examples are planned for artifact-backed serving.</p>
    </>
  );
}
