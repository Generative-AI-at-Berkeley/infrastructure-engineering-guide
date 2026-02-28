# CI Pipeline

**The Problem**
Without CI, every PR becomes a manual test session. People forget to run linters, tests are flaky, and bugs slip through. In monorepos it gets worse because every tiny change triggers everything, and CI becomes slow and expensive.

> Hilary is about to send a really really risky text to her crush she met on Hinge. She thinks it'll green so she full sends with a text saying "do you want to go get sushi in SF? the fish there is really really fresh and the otoro tastes better than the ones they serve in Japan

> She forgot that boy was highly fatally allergic to seafood

> gg

> Hilary sets up a CI, and in the CI she makes sure to check every single risky text against a collection of rules and things to avoid.

> When hilary asks her next hinge date out (since the last hinge date she literally proposed 1st degree manslaughter), the risky text is automatically checked against everything, including allergies. so every single time she will know if a text will green or not.

**The Solution**
Use GitHub Actions with path filtering to run only the relevant checks. Spin up real service containers (Postgres) so tests run against the same dependencies you use in production. Gate merges on a single `check` command that includes linting, formatting, type checks, circular dependency checks, and unused export checks.

**Real Code**
Here is a CI workflow with path filtering and service containers. Every non-obvious line is annotated.

```yaml
name: ci
on:
  pull_request:

jobs:
  changes:
    runs-on: ubuntu-latest
    outputs:
      backend: ${{ steps.filter.outputs.backend }}
    steps:
      - uses: actions/checkout@v4
      - id: filter
        uses: dorny/paths-filter@v3
        with:
          filters: |
            backend:
              - "backend/**"
              - "package.json"
              - "package-lock.json"
              - ".github/workflows/ci.yml"

  backend:
    needs: changes
    if: needs.changes.outputs.backend == 'true' # Skip when backend did not change.
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: app
          POSTGRES_PASSWORD: app
          POSTGRES_DB: app_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd="pg_isready -U app -d app_test"
          --health-interval=5s
          --health-timeout=5s
          --health-retries=10
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install
        run: npm ci

      - name: Check
        env:
          DATABASE_URL: postgres://app:app@localhost:5432/app_test
        run: npm run check # Aggregates lint, typecheck, format, and other gates.

      - name: Test
        env:
          DATABASE_URL: postgres://app:app@localhost:5432/app_test
        run: npm test
```

**Key Lessons**
- Path filtering makes CI fast and cheap without losing coverage.
- Service containers give you real dependencies, not mocks.
- A single `npm run check` gate is a strong discipline. Everything passes or the PR does not merge.
- Health checks prevent flaky test failures from racing the database boot.

**How This Applies Elsewhere**
GitHub Actions is common for startups, but the pattern works in CircleCI, Buildkite, and GitLab CI. Path filtering, service containers, and a single quality gate are universal ideas.
