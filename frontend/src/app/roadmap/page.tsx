import { PageIntro } from "@/components/common/page-intro";
import { Card } from "@/components/ui/card";

const milestones = [
  ["M00", "Foundation and scaffold"], ["M01", "Data layer"], ["M02", "Classical baselines and metrics"],
  ["M03", "Feature reduction"], ["M04", "QSVM core"], ["M05", "Quantum diagnostics"],
  ["M06", "Hybrid quantum neural network"], ["M07", "Cascade and cost policy"], ["M08", "Serving"],
  ["M09", "Dashboard completion"], ["M10", "Robustness and scale"], ["M11", "Hardening and release"],
] as const;

export default function RoadmapPage() {
  return <>
    <PageIntro title="Development roadmap" description="From the placeholder scaffold through validated serving and release." />
    <Card><ol className="trace">
      {milestones.map(([id, name]) => <li key={id}>
        <strong>{id} · {name}</strong>{" "}
        <span className="muted">{id === "M00" ? "Scaffolded (stub)" : "Planned"}</span>
      </li>)}
    </ol></Card>
  </>;
}
