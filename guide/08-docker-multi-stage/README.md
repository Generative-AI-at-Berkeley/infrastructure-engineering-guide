# Docker Multi-Stage Builds

**The Problem**
If you ship the same image you build with, your production container contains dev dependencies, build tools, and half the internet. That makes images huge, slow to deploy, and a bigger security target.

> Emily's roommates want to play with her bunnies again, so she needs to bring her bunnies from SF to Berkeley. The problem is that the bunnies need a literbox, hay, pellets, water, and fresh fruit and vegetables. So doing this even once is extremely slow and time consuming.

> So to fix this, Enily builds them the litterbox, puts the hay in, and prepare the water and fruit in Berkeley, so when she wants to move the bunnies all she needs to do is put them in a small carrier and bring them over.

**The Solution**
Use multi-stage builds. Install full dependencies once, build the app, then copy only the runtime artifacts and production dependencies into the final image. Smaller, faster, safer.

**Real Code**
Below is a 4-stage Dockerfile with annotations for every non-obvious line.

```Dockerfile
# 1) deps: install all dependencies (including dev)
FROM node:20-bookworm AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci # Full dependency install for build.

# 2) prod-deps: install prod-only dependencies
FROM node:20-bookworm AS prod-deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev # Smaller node_modules for runtime only.

# 3) build: compile the app
FROM node:20-bookworm AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build # Produces dist/ or build/ artifacts.

# 4) final: tiny runtime image
FROM node:20-slim AS final
WORKDIR /app
ENV NODE_ENV=production
COPY --from=prod-deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./package.json
EXPOSE 8080
CMD ["node", "dist/server.js"]
```

**Key Lessons**
- Separate build-time dependencies from runtime dependencies.
- Copy only the built artifacts into the final image.
- Docker layer caching works best when you copy lockfiles before app code.
- Smaller images reduce attack surface and deploy faster.

**How This Applies Elsewhere**
The exact steps vary by language, but the pattern is the same for Go, Python, Java, and Rust. Build in one stage, run in another.
