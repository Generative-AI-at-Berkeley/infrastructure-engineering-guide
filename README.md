# How Real Apps Ship

This repo is a guided walkthrough of production infrastructure. It is built for CS students who can code but have never shipped.

**Start Here**
Do the hands-on lab first:
- `hands-on/README.md`

It is small, real, and runnable. You will start Postgres, run migrations, and touch real data.

**Deep Dives**
Each folder explains one production layer with real code examples:
- `guide/01-docker-compose/`
- `guide/02-mise/`
- `guide/03-python-tooling/`
- `guide/04-schema-and-migrations/`
- `guide/05-ci-pipeline/`
- `guide/06-deployment-pipeline/`
- `guide/07-keyless-auth/`
- `guide/08-docker-multi-stage/`
- `guide/09-infrastructure-as-code/`

**How To Replicate This Infrastructure (Copy/Paste Plan)**
If you want to bring these patterns into your own project:
1. Add a `docker-compose.yml` that mirrors your dependencies. See `guide/01-docker-compose/`.
2. Pin tool versions and create one-command tasks. See `guide/02-mise/` for the pattern (mise/asdf/Makefile all work).
3. Lock Python deps and enforce a single quality gate. See `guide/03-python-tooling/`.
4. Add numbered migrations and run them before deploy. See `guide/04-schema-and-migrations/`.
5. Add CI that runs only what changed. See `guide/05-ci-pipeline/`.
6. Add a chained deploy workflow. See `guide/06-deployment-pipeline/`.
7. Use OIDC so CI can deploy without keys. See `guide/07-keyless-auth/`.
8. Use multi-stage Docker so prod images are small and safe. See `guide/08-docker-multi-stage/`.
9. Add IaC when you are ready. See `guide/09-infrastructure-as-code/`.

**Why This Matters**
A good codebase is not clever code. It is infrastructure that makes teams fast and safe. The UI framework will change every 3 years. These patterns will not.
