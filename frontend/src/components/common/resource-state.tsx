export function ResourceState({ loading, error, empty = false }: {
  loading?: boolean; error?: Error; empty?: boolean;
}) {
  if (error) return <div className="section-card" role="alert">{error.message}</div>;
  if (loading) return <div className="section-card skeleton" role="status">Loading sample data…</div>;
  if (empty) return <div className="section-card">No sample records are available.</div>;
  return null;
}
