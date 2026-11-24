"use client";

import { useState } from "react";
import { LineBandChart, DataTable, PRCurveChart } from "@/components/charts/charts";
import { PageIntro } from "@/components/common/page-intro";
import { ResourceState } from "@/components/common/resource-state";
import { Card } from "@/components/ui/card";
import { useArtifact } from "@/hooks/use-artifact";
import { inr, percent } from "@/lib/format";

const fields = [
  ["pr_auc", "Average precision"], ["recall_at_fixed_fpr", "Recall at fixed FPR"], ["f1", "F1"], ["mcc", "MCC"],
] as const;

export default function ComparisonPage() {
  const { data, error, isLoading } = useArtifact("/api/models/comparison");
  const ablations = useArtifact("/api/models/ablations");
  const [sort, setSort] = useState<typeof fields[number][0]>("pr_auc");
  const model = data?.data;
  if (!model) return <><PageIntro title="Model comparison" description="Review illustrative benchmark results." />
    <ResourceState loading={isLoading} error={error} empty /></>;
  const rows = [...model.metrics].sort((a, b) => b[sort] - a[sort]);
  const baseline = model.costs.find(item => item.policy === "Classical")?.expected_cost_inr;
  return (
    <>
      <PageIntro title="Model comparison" description="Explore matched metrics, operating curves, and review cost." />
      <Card>
        <h2>Benchmark metrics</h2>
        <label>Sort by
          <select value={sort} onChange={event => setSort(event.target.value as typeof sort)}>
            {fields.map(([key, label]) => <option key={key} value={key}>{label}</option>)}
          </select>
        </label>
        <div className="table-scroll"><DataTable headers={["Model", ...fields.map(([, l]) => l)]}
          rows={rows.map(row => [row.model, ...fields.map(([k]) => row[k].toFixed(3))])} /></div>
      </Card>
      <div className="grid-cards">
        <PRCurveChart points={model.pr_curve} />
        <LineBandChart title="ROC curve" description="Illustrative distinction across operating points."
          points={model.roc_curve} xLabel="False-positive rate" yLabel="Recall" />
      </div>
      <LineBandChart title="Recall vs quantum load" description="Routing tradeoff implied by the sample curves."
        points={model.routing} xLabel="Routed share" yLabel="Recall" />
      <Card><h2>Cost comparison</h2>
        <DataTable headers={["Policy", "Expected cost", "Savings vs classical"]}
          rows={model.costs.map(c => [c.policy, inr.format(c.expected_cost_inr),
            baseline === undefined ? "—" : inr.format(baseline - c.expected_cost_inr)])} />
      </Card>
      <Card><h2>Matched ablations</h2>
        {ablations.data ? <DataTable headers={["Policy", "AP change", "Routed"]} rows={ablations.data.data.rows.map(
          row => [row.policy, row.pr_auc_delta.toFixed(3), percent.format(row.routed_share)]
        )} /> : <ResourceState loading={ablations.isLoading} error={ablations.error} empty />}
      </Card>
    </>
  );
}
