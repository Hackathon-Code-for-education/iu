FROM node:20.12-slim as base

WORKDIR /app

# Build
FROM base as build

COPY --link package.json pnpm-lock.yaml ./
RUN yarn global add pnpm && pnpm i --frozen-lockfile

COPY --link . .

RUN pnpm run build
RUN pnpm prune

# Run
FROM base

ENV NODE_ENV=production

COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/.output /app/.output

CMD [ "node", ".output/server/index.mjs" ]
