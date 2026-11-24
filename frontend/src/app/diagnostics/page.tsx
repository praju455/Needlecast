"use client";

import { useState } from "react";
import { BarChart, DataTable, HeatmapChart } from "@/components/charts/charts";
import { PageIntro } from "@/components/common/page-intro";
import { ResourceState } from "@/components/common/resource-state";
import { Card } from "@/components/ui/card";
import { useArtifact } from "@/hooks/use-artifact";
import { percent } from "@/lib/format";

const topics = ["Circuits", "Kernel", "HQNN", "Noise"] as const;

function Circuits() {
  const { data, error, isLoading } = useArtifact("/api/diagnostics/circuits");
  const circuits = data?.data.circuits;
  if (!circuits?.length) return <ResourceState loading={isLoading} error={error} empty />;
  return (
    <Card>
      <h2>Circuit register</h2>
      <DataTable headers={["Circuit", "Width", "Depth", "Gates", "Transpiled depth"]}
        rows={circuits.map(c => [c.name, c.width, c.depth, c.gates, c.transpiled_depth])} />
      <div className="grid-cards">
        {circuits.map(c => <object type="image/svg+xml" key={c.name} data={c.svg_url}
          aria-label={`${c.name} placeholder circuit`} width="100%" height="140">
          <a href={c.svg_url}>View {c.name}</a>
        </object>)}
      </div>
    </Card>
  );
}

function Kernel() {
  const { data, error, isLoading } = useArtifact("/api/diagnostics/kernel");
  if (!data) return <ResourceState loading={isLoading} error={error} empty />;
  return <>
    <HeatmapChart matrix={data.data.matrix} />
    <BarChart title="Kernel concentration" description="Illustrative off-diagonal variance by qubit width."
      data={data.data.concentration} />
    <Card>Variance {data.data.variance.toFixed(4)} · Alignment {data.data.alignment.toFixed(4)}</Card>
  </>;
}

function Hqnn() {
  const { data, error, isLoading } = useArtifact("/api/diagnostics/hqnn");
  if (!data) return <ResourceState loading={isLoading} error={error} empty />;
  return <BarChart title="Gradient variance" description="Sample variance by trainable circuit layer."
    data={data.data.gradient_variance} />;
}

function Noise() {
  const { data, error, isLoading } = useArtifact("/api/diagnostics/noise");
  if (!data) return <ResourceState loading={isLoading} error={error} empty />;
  return <BarChart title="Recall by shot count" description={`Illustrative ideal recall is ${percent.format(data.data.ideal_recall)}.`}
    data={data.data.shot_recall} />;
}

export default function DiagnosticsPage() {
  const [tab, choose] = useState<typeof topics[number]>("Circuits");
  const sections = { Circuits, Kernel, HQNN: Hqnn, Noise };
  const Details = sections[tab];
  return <>
    <PageIntro title="Diagnostics" description="Inspect circuit structure, kernel similarities, gradients, and shot sensitivity." />
    <fieldset className="section-card actions">
      <legend>Diagnostic view</legend>
      {topics.map(topic => <label className="inline-flex items-center gap-2" key={topic}>
        <input type="radio" name="topic" value={topic} checked={topic === tab} onChange={() => choose(topic)} />
        {topic}
      </label>)}
    </fieldset>
    <Details />
  </>;
}
