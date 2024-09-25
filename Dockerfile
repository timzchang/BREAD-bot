# syntax = docker/dockerfile:1

# Adjust NODE_VERSION as desired
ARG NODE_VERSION=22.9.0
FROM node:${NODE_VERSION}-slim AS base

LABEL fly_launch_runtime="Node.js"

# Node.js app lives here
WORKDIR /app

# Set production environment
ENV NODE_ENV="production"


# Throw-away build stage to reduce size of final image
FROM base AS build

# Install packages needed to build node modules
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential node-gyp pkg-config python-is-python3

# Install node modules
COPY --link package-lock.json package.json ./
RUN npm ci --include=dev

# Copy application code
COPY --link . .

# Build application
RUN npm run build

# Remove development dependencies
RUN npm prune --omit=dev


# Final stage for app image
FROM base

# Copy built application
#13 [build 5/7] RUN ls
#13 0.159 Dockerfile
#13 0.159 LICENSE
#13 0.159 README.md
#13 0.159 assets
#13 0.159 build
#13 0.159 commands.js
#13 0.159 examples
#13 0.159 fly.toml
#13 0.159 game.js
#13 0.159 lib
#13 0.159 node_modules
#13 0.159 old-app.js
#13 0.159 package-lock.json
#13 0.159 package.json
#13 0.159 renovate.json
#13 0.159 src
#13 0.159 tsconfig.json
#13 0.159 utils.js
COPY --from=build /app/build /app/build
COPY --from=build /app/package.json /app/package.json
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/assets /app/assets

# Start the server by default, this can be overwritten at runtime
EXPOSE 3000
CMD [ "npm", "run", "start" ]
