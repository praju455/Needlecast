"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

const sections = [
  ["/", "Overview"], ["/data", "Datasets"], ["/reduction", "Feature reduction"],
  ["/scoring", "Scoring"], ["/comparison", "Model comparison"],
  ["/diagnostics", "Diagnostics"], ["/roadmap", "Roadmap"],
] as const;

export function Navigation() {
  const path = usePathname();
  return (
    <nav aria-label="Workspace" className="workspace-nav">
      {sections.map(([href, label]) => (
        <Link key={href} href={href} aria-current={href === path ? "page" : undefined}>{label}</Link>
      ))}
    </nav>
  );
}

export function ThemeToggle() {
  const [selected, setSelected] = useState<"light" | "dark" | null>(null);
  function toggle() {
    const dark = selected ? selected === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
    const theme = dark ? "light" : "dark";
    document.documentElement.dataset.theme = theme;
    setSelected(theme);
  }
  return <button className="theme-toggle" type="button" onClick={toggle}>Switch theme</button>;
}
