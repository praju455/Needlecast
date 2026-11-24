import type { Metadata } from "next";
import Link from "next/link";

import { PlaceholderBanner } from "@/components/common/placeholder-banner";
import { Navigation, ThemeToggle } from "@/components/layout/navigation";

import "./globals.css";

export const metadata: Metadata = {
  title: { default: "Needlecast", template: "%s | Needlecast" },
  description: "Hybrid fraud-detection research workspace",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <a className="skip" href="#workspace-content">Skip to content</a>
        <header className="topbar">
          <Link className="brand" href="/"><span className="mark" aria-hidden="true">N</span>Needlecast</Link>
          <ThemeToggle />
        </header>
        <div className="workspace">
          <Navigation />
          <main id="workspace-content">
            <PlaceholderBanner />
            {children}
            <footer>Needlecast <span>v{process.env.NEXT_PUBLIC_APP_VERSION}</span></footer>
          </main>
        </div>
      </body>
    </html>
  );
}
