# Docker Compose

**The Problem**
Without containers, every developer has a different Postgres, a different Redis, and usually no local S3 or email at all. That means your code works on your laptop and breaks the moment it touches a real dependency. You cannot debug what you cannot reproduce.

**The Solution**
Use Docker Compose to mirror production dependencies locally. Give every developer the same Postgres, the same object storage, and the same SMTP sink. This is how you turn "works on my machine" into "works on the team."

**Real Code**
Below is a full `docker-compose.yml` with annotations for every non-obvious line. This mirrors a common production stack: Postgres, Redis, S3-compatible storage (MinIO), and email (Mailpit).

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:15
    container_name: valdera-postgres
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
      POSTGRES_DB: app
    ports:
      - "5432:5432" # Map host port for local tools like psql or GUI clients.
    volumes:
      - db-data:/var/lib/postgresql/data # Named volume keeps data between restarts.
      - ./docker/initdb.d:/docker-entrypoint-initdb.d:ro # Seed schemas and roles on first boot.
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app -d app"]
      interval: 5s
      timeout: 5s
      retries: 10

  redis:
    image: redis:7
    container_name: valdera-redis
    ports:
      - "6379:6379" # Local cache and queue dev.

  minio:
    image: minio/minio:RELEASE.2024-02-17T01-15-57Z
    container_name: valdera-minio
    environment:
      MINIO_ROOT_USER: minio
      MINIO_ROOT_PASSWORD: minio123
    command: server /data --console-address ":9001" # Serve S3 API and web console.
    ports:
      - "9000:9000" # S3-compatible API endpoint.
      - "9001:9001" # MinIO web console.
    volumes:
      - minio-data:/data # Persist buckets across restarts.

  mailpit:
    image: axllent/mailpit:v1.15
    container_name: valdera-mailpit
    ports:
      - "1025:1025" # SMTP server your app sends to.
      - "8025:8025" # Web UI to view emails.

volumes:
  db-data:
  minio-data:
```

**Key Lessons**
- Named volumes make your local database durable. Containers can be killed and recreated without data loss.
- `initdb.d` scripts let you seed roles, extensions, and schemas once, exactly like production.
- MinIO gives you real S3 semantics locally, so you are not mocking storage logic.
- Mailpit captures outbound email safely. You test email flows without sending real mail.
- The goal is not "run containers." The goal is "make dev look like prod."

**How This Applies Elsewhere**
Docker Compose is the most common tool, but the pattern is universal. Devcontainers, Tilt, Skaffold, and even Kubernetes-in-Docker all solve the same problem: consistent local dependencies.
