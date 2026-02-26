# Deployment Pipeline

**The Problem**
Deploys done by hand are slow, inconsistent, and risky. If you deploy code before running migrations, you ship a guaranteed outage. If every deploy is a snowflake, you cannot roll back or reason about what happened.

> even tho hilary already set up a CI, she lowkey has anxiety and makes a pipeline so that --> WHEN the text succeeds after being checked against the rules she set, it gets automatically sent to a Andrea with the right context to get a second opinion before manually sending it to her crush. 

**The Solution**
Use a chained deployment workflow. CI success triggers staging deploys. Production deploys are a manual merge to `prod`. Migrations run before deploys with `wait: true`. Images are dual tagged so you can always trace the exact commit that shipped. Concurrency control prevents overlapping deploys.

**Real Code**
Here is a deployment workflow that matches the real pattern. Every non-obvious line is annotated.

```yaml
name: deploy
on:
  workflow_run:
    workflows: ["ci"]
    types: [completed]

concurrency:
  group: deploy-${{ github.ref }} # Only one deploy per branch at a time.
  cancel-in-progress: false

jobs:
  stage:
    if: >-
      github.event.workflow_run.conclusion == 'success' &&
      github.event.workflow_run.head_branch == 'main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            gcr.io/example/app:latest
            gcr.io/example/app:${{ github.event.workflow_run.head_sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max # Layer cache speeds up rebuilds.

      - name: Run migrations
        run: ./scripts/migrate --env=stage --wait=true # Block until migrations finish.

      - name: Deploy to stage
        run: ./scripts/deploy --env=stage --image=gcr.io/example/app:${{ github.event.workflow_run.head_sha }}

  prod:
    if: github.event.workflow_run.head_branch == 'prod' && github.event.workflow_run.conclusion == 'success'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run migrations
        run: ./scripts/migrate --env=prod --wait=true
      - name: Deploy to prod
        run: ./scripts/deploy --env=prod --image=gcr.io/example/app:${{ github.event.workflow_run.head_sha }}
```

**Key Lessons**
- Chained workflows make deploys deterministic. CI success is the only trigger.
- Migrations must run before code deploys, always, and you wait for them to finish.
- Dual tags (`latest` and commit SHA) make rollbacks and audits easy.
- Concurrency control prevents overlapping deploys and weird race conditions.
- When your container platform redeploys, it sends SIGTERM. You have about 10 seconds to close database connections and finish in-flight requests. Always handle it.

**How This Applies Elsewhere**
GitHub Actions is one implementation. The same pipeline exists in Buildkite, Argo, GitLab, and Jenkins. The sequence is the point: build, migrate, deploy, with one consistent trigger.
