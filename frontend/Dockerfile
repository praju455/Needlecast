FROM node:24-bookworm-slim AS dependencies
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --legacy-peer-deps && npm run setup:integrations

FROM node:24-bookworm-slim AS build
ARG BACKEND_URL=http://backend:8000
ENV NEXT_TELEMETRY_DISABLED=1 BACKEND_URL=$BACKEND_URL
WORKDIR /app
COPY VERSION ./
COPY --from=dependencies /app/frontend/node_modules frontend/node_modules
COPY frontend frontend
WORKDIR /app/frontend
RUN npm run build

FROM node:24-bookworm-slim AS runner
ENV NODE_ENV=production NEXT_TELEMETRY_DISABLED=1 HOSTNAME=0.0.0.0
WORKDIR /app
COPY --from=build --chown=node:node /app/frontend/.next/standalone ./
COPY --from=build --chown=node:node /app/frontend/.next/static ./frontend/.next/static
USER node
EXPOSE 3000
CMD ["node", "frontend/server.js"]
