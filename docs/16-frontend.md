# Dashboard scaffold

The Next.js App Router serves one workspace. The footer reads the project version. The responsive navigation includes seven views.

| Page | API or source |
| --- | --- |
| `/` | Datasets and comparison fixtures |
| `/data` | `GET /api/datasets` |
| `/reduction` | `GET /api/pipeline/reduction` |
| `/scoring` | `POST /api/score` |
| `/comparison` | `GET /api/models/comparison` and `GET /api/models/ablations` |
| `/diagnostics` | Circuit, kernel, HQNN, and noise diagnostic reads |
| `/roadmap` | Typed roadmap summary matching M00 through M11 |

Browser calls use the same-origin Next.js rewrite via `BACKEND_URL`. SWR handles read caching, deduplication, and loading state. Scoring uses an explicit non-cached POST with a typed client, a timeout, and safe error messages.

ECharts renders charts through a client-only wrapper. Each chart includes a data table. The integration install enables ECharts. The local component setup follows the shadcn/ui manual layout. The sample banner is persistent across all pages in M00.

See the [developer guide](21-developer-guide.md) for integration setup and the [placeholder data policy](stub-data-policy.md) for labeling.
