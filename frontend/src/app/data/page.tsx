"use client";

import { useState } from "react";

import { BarChart, DataTable } from "@/components/charts/charts";
import { PageIntro } from "@/components/common/page-intro";
import { ResourceState } from "@/components/common/resource-state";
import { Card } from "@/components/ui/card";
import { useArtifact } from "@/hooks/use-artifact";
import { count, percent } from "@/lib/format";

export default function DataPage() {
  const { data, error, isLoading } = useArtifact("/api/datasets");
  const [selection, select] = useState("");
  const datasets = data?.data.datasets ?? [];
  const dataset = datasets.find(item => item.id === selection) ?? datasets[0];
  return (
    <>
      <PageIntro title="Datasets" description="Inspect sample class balance across chronological splits." />
      {!dataset ? <ResourceState loading={isLoading} error={error} empty /> : <>
        <Card>
          <label>Dataset
            <select value={dataset.id} onChange={event => select(event.target.value)}>
              {datasets.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
            </select>
          </label>
          <p className="muted">{dataset.source}</p>
          <DataTable headers={["Window", "Rows", "Fraud", "Prevalence"]}
            rows={dataset.splits.map(r => [r.window, count.format(r.rows), r.fraud, percent.format(r.fraud / r.rows)])} />
        </Card>
        <BarChart title="Fraud by split" description="Illustrative positive class counts."
          data={dataset.splits.map(row => ({ label: row.window, value: row.fraud }))} />
      </>}
    </>
  );
}
