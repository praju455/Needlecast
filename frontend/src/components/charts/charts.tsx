"use client";

import dynamic from "next/dynamic";
import type { ReactNode } from "react";

const ECharts = dynamic(() => import("echarts-for-react"), {
  ssr: false,
  loading: () => <p role="status">Loading chart…</p>,
});

type Point = { x: number; y: number; low?: number | null; high?: number | null };
type Trend = { label: string; value: number };

function Chart({ title, description, option, table }: {
  title: string; description: string; option: object; table: ReactNode;
}) {
  return (
    <figure className="section-card">
      <figcaption><h2>{title}</h2><p className="muted">{description}</p></figcaption>
      <div aria-label={title} role="img">
        <ECharts option={{ aria: { enabled: true }, color: ["#238d78", "#846bce", "#18374b"], ...option }}
          style={{ height: "300px", width: "100%" }} notMerge />
      </div>
      <details open={process.env.NEXT_PUBLIC_CHARTS_AVAILABLE === "false" ? true : undefined}>
        <summary>View data</summary>
        <div className="table-scroll">{table}</div>
      </details>
    </figure>
  );
}

export function DataTable({ headers, rows }: {
  headers: readonly string[]; rows: ReadonlyArray<ReadonlyArray<ReactNode>>;
}) {
  return (
    <table>
      <thead><tr>{headers.map(header => <th key={header} scope="col">{header}</th>)}</tr></thead>
      <tbody>{rows.map((row, i) => (
        <tr key={i}>{row.map((cell, index) => <td key={index}>{cell}</td>)}</tr>
      ))}</tbody>
    </table>
  );
}

export function BarChart({ title, description, data }: { title: string; description: string; data: Trend[] }) {
  return (
    <Chart title={title} description={description}
      option={{
        xAxis: { type: "category", data: data.map(item => item.label) },
        yAxis: { type: "value" }, tooltip: {},
        series: [{ type: "bar", data: data.map(item => item.value) }],
      }}
      table={<DataTable headers={["Category", "Value"]} rows={data.map(i => [i.label, i.value])} />} />
  );
}

export function LineBandChart({ title, description, points, xLabel, yLabel }: {
  title: string; description: string; points: Point[]; xLabel: string; yLabel: string;
}) {
  const interval = points.length > 0 && points.every(point => point.low != null && point.high != null);
  const xAxis = interval
    ? { type: "category", name: xLabel, boundaryGap: false, data: points.map(p => p.x) }
    : { type: "value", name: xLabel, min: 0, max: 1 };
  const band = interval ? [
    { type: "line", stack: "interval", symbol: "none", lineStyle: { opacity: 0 },
      data: points.map(point => point.low) },
    { type: "line", stack: "interval", symbol: "none", lineStyle: { opacity: 0 },
      areaStyle: { opacity: 0.18 }, data: points.map(point => (point.high ?? 0) - (point.low ?? 0)) },
  ] : [];
  return (
    <Chart title={title} description={description}
      option={{
        tooltip: { trigger: "axis" }, xAxis,
        grid: { left: 45, right: 100, bottom: 45, top: 45 },
        yAxis: { type: "value", name: yLabel, min: 0, max: 1 },
        series: [
          ...band,
          { type: "line", showSymbol: false, data: points.map(p => interval ? p.y : [p.x, p.y]) },
        ],
      }}
      table={<DataTable headers={interval ? [xLabel, yLabel, "Lower", "Upper"] : [xLabel, yLabel]}
        rows={points.map(p => interval ? [p.x, p.y.toFixed(3), p.low?.toFixed(3), p.high?.toFixed(3)]
          : [p.x, p.y.toFixed(3)])} />} />
  );
}

export function PRCurveChart({ points }: { points: Point[] }) {
  return <LineBandChart title="Precision–recall" description="Illustrative curve and interval."
    points={points} xLabel="Recall" yLabel="Precision" />;
}

export function HeatmapChart({ matrix }: { matrix: number[][] }) {
  const axes = matrix.map((_, i) => i);
  const values = matrix.flatMap((row, y) => row.map((value, x) => [x, y, value]));
  const sample = matrix.slice(0, 8).map(row => row.slice(0, 8));
  return (
    <Chart title="Class-sorted kernel" description="Synthetic pairwise similarities from 0 to 1. The table samples the first eight rows and columns."
      option={{
        grid: { left: 40, right: 35, bottom: 42, top: 15 },
        xAxis: { type: "category", data: axes },
        yAxis: { type: "category", data: axes },
        visualMap: { min: 0, max: 1, show: false, inRange: { color: ["#f0f5fa", "#81cbbb", "#173b56"] } },
        tooltip: {},
        series: [{ type: "heatmap", data: values }],
      }}
      table={<DataTable headers={["Row", ...axes.slice(0, 8).map(String)]}
        rows={sample.map((row, i) => [i, ...row])} />} />
  );
}
