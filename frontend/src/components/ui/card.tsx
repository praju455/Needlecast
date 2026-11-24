import type { ComponentProps } from "react";

export function Card({ className, ...props }: ComponentProps<"section">) {
  return <section data-slot="card" className={`section-card ${className ?? ""}`} {...props} />;
}

export function CardTitle(props: ComponentProps<"h2">) {
  return <h2 data-slot="card-title" {...props} />;
}
