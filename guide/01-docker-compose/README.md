# Docker Compose

**The Problem**
Without containers, every developer has a different Postgres, a different Redis, and usually no local S3 or email at all. That means your code works on your laptop and breaks the moment it touches a real dependency. You cannot debug what you cannot reproduce.

> Alex De Saram goes on a date with a girl from an AGC, and he tells her that he can cook really well, so she asks him to come over to cook this weekend.

> The issue is he can't cook.

> So he watches youtube and tiktok videos on how to cook, but since he doesn't have a kitchen at home he couldn't practice and lowkgenuinely cooks up the most henious atrocity known to man and gets ghosted.

> With docker, he still has a kitchen locally, so he can watch the videos, cook it up in real time, test the food to see if it tastes good or needs adjustments, so when he goes on his date he cooks literally and figuratively.

**The Solution**
Use Docker Compose to mirror production dependencies locally. Give every developer the same Postgres, the same object storage, and the same SMTP sink. This is how you turn "works on my machine" into "works on the team."

**Real Code**
Below is a full `docker-compose.yml` with annotations for every non-obvious line. This mirrors a common production stack: Postgres, Redis, S3-compatible storage (MinIO), and email (Mailpit).

```yaml
version: "3.9"

services:
  db:
    image: postgres:15
    container_name: example-db
    environment:
      POSTGRES_USER: devuser
      POSTGRES_PASSWORD: devpass
      POSTGRES_DB: devdb
    ports:
      - "5432:5432" # Exposes Postgres for your local tools.
    volumes:
      - database-data:/var/lib/postgresql/data # Keeps DB data persistent across restarts.
      - ./docker/initdb.d:/docker-entrypoint-initdb.d:ro # Auto-runs schema and seed scripts at startup.
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devuser -d devdb"]
      interval: 5s
      timeout: 5s
      retries: 10

  cache:
    image: redis:7
    container_name: example-redis
    ports:
      - "6379:6379" # Exposes Redis for your app and debugging.

  objectstore:
    image: minio/minio:RELEASE.2024-02-17T01-15-57Z
    container_name: example-minio
    environment:
      MINIO_ROOT_USER: miniouser
      MINIO_ROOT_PASSWORD: miniopass
    command: server /data --console-address ":9001" # S3-compatible storage and UI console.
    ports:
      - "9000:9000" # S3 API endpoint
      - "9001:9001" # MinIO Web Console
    volumes:
      - objectstore-data:/data # Keeps buckets and objects persistent

volumes:
  database-data:
  objectstore-data:
```


**Key Lessons**
- Named volumes make your local database durable. Containers can be killed and recreated without data loss.
- `initdb.d` scripts let you seed roles, extensions, and schemas once, exactly like production.
- MinIO gives you real S3 semantics locally, so you are not mocking storage logic.
- The goal is not "run containers." The goal is "make dev look like prod."

**How This Applies Elsewhere**
Docker Compose is the most common tool, but the pattern is universal. Devcontainers, Tilt, Skaffold, and even Kubernetes-in-Docker all solve the same problem: consistent local dependencies.
