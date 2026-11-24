# Developer guide

Use Python 3.11–3.13, Node.js 22 or newer, npm, and Make. Start from the repository root.

```bash
make setup
make sample-artifacts
make dev
```

The dashboard uses port 3000 and the API uses port 8000. Set `BOOTSTRAP_PYTHON` to choose a compatible Python executable. To use an existing compatible environment, pass `PYTHON=/path/to/python` to Make.

```bash
make setup-integrations
make lint
make typecheck
make test
make validate-artifacts
make types
make docs-check
```

The integration install adds pinned ECharts, the official OpenAPI generator, and Playwright packages. When the chart packages are unavailable, the dashboard displays the chart source tables. `make types` writes checked-in declarations from the exported contract. `make types-official` additionally runs the official CLI on the same schema. To run browser checks, install Playwright's browser with `cd frontend && npx playwright install chromium`, then run `npm --prefix frontend run smoke` from the root while the app is running. `make api-check` exercises the running HTTP service and prints two sample routes.

For containers, generate the sample artifacts first, then run `make up`. Use `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build` for bind mounts and hot reload. `make down` stops the normal stack. See [serving and deployment](serving-and-deployment.md) for production work.
