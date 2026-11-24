"use client";

import { BarChart, DataTable } from "@/components/charts/charts";
import { PageIntro } from "@/components/common/page-intro";
import { ResourceState } from "@/components/common/resource-state";
import { Card } from "@/components/ui/card";
import { useArtifact } from "@/hooks/use-artifact";

export default function ReductionPage() {
  const { data, error, isLoading } = useArtifact("/api/pipeline/reduction");
  const model = data?.data;
  return (
    <>
      <PageIntro title="Feature reduction" description="Inspect the feature schema and the projected circuit inputs." />
      {!model ? <ResourceState error={error} loading={isLoading} empty /> : <>
        <Card>
          <h2>{model.reducer}</h2>
          <p>{model.input_dimensions} input features → {model.output_dimensions} ordered angles</p>
          <DataTable headers={["Feature", "Qubit"]} rows={model.features.map((item, i) => [item, i])} />
        </Card>
        <BarChart title="Explained variance" description="Illustrative share of input variance by component."
          data={model.explained_variance.map((value, i) => ({ label: model.features[i] ?? String(i + 1), value }))} />
      </>}
    </>
  );
}
