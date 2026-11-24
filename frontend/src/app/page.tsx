"use client";

import { PageIntro } from "@/components/common/page-intro";
import { ResourceState } from "@/components/common/resource-state";
import { Card, CardTitle } from "@/components/ui/card";
import { useArtifact } from "@/hooks/use-artifact";
import { count, percent } from "@/lib/format";

export default function Overview() {
  const datasets = useArtifact("/api/datasets");
  const comparison = useArtifact("/api/models/comparison");
  const rows = datasets.data?.data.datasets[0]?.splits;
  const test = rows?.find(row => row.window === "Test");
  const metric = comparison.data?.data.metrics.find(item => item.model === "Cascade");
  return (
    <>
      <PageIntro title="Fraud detection workspace" description="Compare classical and hybrid scoring at a defined review budget." />
      <ResourceState loading={datasets.isLoading || comparison.isLoading}
        error={datasets.error ?? comparison.error} empty={!test && !metric} />
      {(test || metric) && <div className="grid-cards">
        {test && <Card className="metric"><span>Sample test transactions</span><strong>{count.format(test.rows)}</strong></Card>}
        {test && <Card className="metric"><span>Sample fraud prevalence</span><strong>{percent.format(test.fraud / test.rows)}</strong></Card>}
        {metric && <Card className="metric"><span>Illustrative cascade average precision</span><strong>{percent.format(metric.pr_auc)}</strong></Card>}
      </div>}
      <Card>
        <CardTitle>Scoring pipeline</CardTitle>
        <p>The classical model screens all transactions. An uncertainty band routes eligible cases to a bounded second opinion. The scoring trace records the route and review decision.</p>
      </Card>
    </>
  );
}
