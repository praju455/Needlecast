"use client";

import useSWR from "swr";

import { readApi } from "@/lib/api";

export function useArtifact<P extends Parameters<typeof readApi>[0]>(path: P) {
  return useSWR(path, readApi<P>, { shouldRetryOnError: false });
}
