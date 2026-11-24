// Generated from backend/openapi.json by scripts/export_types.py.
export interface components {
  schemas: {
    "Ablation": { "interval": string; "policy": string; "pr_auc_delta": number; "routed_share": number; };
    "Ablations": { "rows": Array<components["schemas"]["Ablation"]>; };
    "Artifact_Ablations_": { "created_at": string; "data": components["schemas"]["Ablations"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Artifact_Circuits_": { "created_at": string; "data": components["schemas"]["Circuits"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Artifact_Comparison_": { "created_at": string; "data": components["schemas"]["Comparison"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Artifact_Datasets_": { "created_at": string; "data": components["schemas"]["Datasets"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Artifact_HQNN_": { "created_at": string; "data": components["schemas"]["HQNN"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Artifact_Kernel_": { "created_at": string; "data": components["schemas"]["Kernel"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Artifact_Noise_": { "created_at": string; "data": components["schemas"]["Noise"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Artifact_Reduction_": { "created_at": string; "data": components["schemas"]["Reduction"]; "dataset_id": string; "disclaimer"?: string | null; "generated_by": string; "mode": "stub" | "live"; "run_id": string; "schema_version": "1"; "seed": number; "split_id": string; };
    "Circuit": { "depth": number; "gates": number; "name": string; "svg_url": string; "transpiled_depth": number; "width": number; };
    "Circuits": { "circuits": Array<components["schemas"]["Circuit"]>; };
    "Comparison": { "costs": Array<components["schemas"]["Cost"]>; "metrics": Array<components["schemas"]["Metric"]>; "pr_curve": Array<components["schemas"]["CurvePoint"]>; "roc_curve": Array<components["schemas"]["CurvePoint"]>; "routing": Array<components["schemas"]["CurvePoint"]>; };
    "Cost": { "expected_cost_inr": number; "policy": string; };
    "Counts": { "fraud": number; "rows": number; "window": string; };
    "CurvePoint": { "high"?: number | null; "low"?: number | null; "x": number; "y": number; };
    "Dataset": { "id": string; "name": string; "source": string; "splits": Array<components["schemas"]["Counts"]>; };
    "Datasets": { "datasets": Array<components["schemas"]["Dataset"]>; };
    "Error": { "code": string; "disclaimer"?: string | null; "message": string; "mode"?: "stub" | "live"; "request_id": string; };
    "Evidence": { "classical"?: Array<string>; "quantum"?: Array<string>; };
    "HQNN": { "gradient_variance": Array<components["schemas"]["Trend"]>; "loss": Array<components["schemas"]["Trend"]>; };
    "HTTPValidationError": { "detail"?: Array<components["schemas"]["ValidationError"]>; };
    "Health": { "disclaimer"?: string | null; "mode"?: "stub" | "live"; "status"?: "ok"; "version": string; };
    "Job": { "disclaimer"?: string | null; "error_code"?: string | null; "id": string; "mode"?: "stub" | "live"; "progress"?: number; "published_run_id"?: string | null; "result_url"?: string | null; "status"?: "queued" | "running" | "succeeded" | "failed"; "status_url": string; };
    "JobRequest": { "dataset_id"?: string; "mode"?: "stub" | "live"; "preset": string; };
    "Kernel": { "alignment": number; "classes": Array<0 | 1>; "concentration": Array<components["schemas"]["Trend"]>; "matrix": Array<Array<number>>; "variance": number; };
    "Metric": { "f1": number; "mcc": number; "model": string; "pr_auc": number; "recall_at_fixed_fpr": number; };
    "Noise": { "ideal_recall": number; "shot_recall": Array<components["schemas"]["Trend"]>; };
    "Reduction": { "explained_variance": Array<number>; "features": Array<string>; "input_dimensions": number; "output_dimensions": number; "reducer": string; "schema_id": string; };
    "ScoreRequest": { "feature_schema_id": string; "mode"?: "stub" | "live"; "transaction": Record<string, unknown>; };
    "ScoreResponse": { "bundle_id": string; "classical": components["schemas"]["ScoredModel"]; "decision": "clear" | "review"; "disclaimer"?: string | null; "evidence"?: components["schemas"]["Evidence"]; "fallback_reason"?: string | null; "final_score": number; "mode"?: "stub" | "live"; "policy_id": string; "quantum": components["schemas"]["ScoredModel"] | null; "request_id": string; "route": "classical_only" | "quantum_rescored" | "classical_fallback"; "schema_version"?: "1"; "stages": Array<components["schemas"]["TraceStage"]>; "threshold": number; };
    "ScoredModel": { "elapsed_ms": number | null; "model_id": string; "score": number; };
    "TraceStage": { "invoked": boolean; "latency_ms": number | null; "name": string; "notes": string; "score": number | null; };
    "Trend": { "label": string; "value": number; };
    "ValidationError": { "loc": Array<string | number>; "msg": string; "type": string; };
  };
}

export interface paths {
  "/api/circuit-assets/{name}": {
    get: {
      responses: {
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
      };
    };
  };
  "/api/datasets": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_Datasets_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/diagnostics/circuits": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_Circuits_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/diagnostics/hqnn": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_HQNN_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/diagnostics/kernel": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_Kernel_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/diagnostics/noise": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_Noise_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/jobs/run": {
    post: {
      requestBody: { content: { "application/json": components["schemas"]["JobRequest"] } };
      responses: {
        202: { content: { "application/json": components["schemas"]["Job"] } };
        409: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["Error"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/jobs/{id}": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Job"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
      };
    };
  };
  "/api/models/ablations": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_Ablations_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/models/comparison": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_Comparison_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/pipeline/reduction": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Artifact_Reduction_"] } };
        404: { content: { "application/json": components["schemas"]["Error"] } };
        422: { content: { "application/json": components["schemas"]["HTTPValidationError"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/api/score": {
    post: {
      requestBody: { content: { "application/json": components["schemas"]["ScoreRequest"] } };
      responses: {
        200: { content: { "application/json": components["schemas"]["ScoreResponse"] } };
        422: { content: { "application/json": components["schemas"]["Error"] } };
        503: { content: { "application/json": components["schemas"]["Error"] } };
      };
    };
  };
  "/health": {
    get: {
      responses: {
        200: { content: { "application/json": components["schemas"]["Health"] } };
      };
    };
  };
}
