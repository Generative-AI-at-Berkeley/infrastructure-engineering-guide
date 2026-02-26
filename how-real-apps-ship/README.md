# Software Engineering Infra Guide

**Setup**
If you're using VS Code, Cursor, Windsurf, or any VS Code fork, install a markdown preview extension so these docs are way easier to read:

To preview any markdown file: `Cmd+Shift+V` (Mac) or `Ctrl+Shift+V` (Windows/Linux). Or open the command palette (`Cmd+Shift+P`) and search "Markdown: Open Preview to the Side".

**What Makes A Good Codebase**
A good codebase is not about clever code. It is about infrastructure that makes the team fast and safe. Can a new engineer clone the repo and be running in 10 minutes? Can you deploy with confidence? Can you roll back? Do your tests actually catch bugs before production?

About 80% of most production is composed of CI pipelines, container builds, database migration strategies, secret management flow, and deployment flow, and only 20% on the code.

**The Layers Of A Production Codebase**

## 1. Docker Compose

**What it is:** A local container stack that mirrors prod dependencies.

**Why you need it:** Your app depends on Postgres, Redis, S3, email, and more. You need those locally or you can't test database connection code.

**How often:** ~90% of production codebases use containers for local dev. So its like, very very very very likely will encounter this.

**Deep dive:** `01-docker-compose/README.md`

## 2. mise

**What it is:** Tool version pinning and task runner in one place.

Think of mise like a master chef's recipe book for your tools: it makes sure everyone on the team uses the exact same ingredients and steps (tool versions and commands), so every dish (your app) comes out the same, every time.

**Why you need it:** Everyone needs the same versions or you will ship bugs that only happen on one laptop.

**How often:** Tool version pinning shows up everywhere. The specific tool varies (mise, asdf, nvm+pyenv) but the pattern is universal. 100% of teams do this in some form.

**Deep dive:** `02-mise/README.md`

## 3. Python tooling (uv, ruff, ty)

**What it is:** Modern Python dependency, lint, and type tooling.

**Why you need it:** Fast, deterministic environments and a single `check` gate that actually enforces quality.

**How often:** If you are writing Python professionally, you will likely encounter `uv` within the next 1 to 2 years. It is rapidly replacing pip. ruff has already replaced flake8+black at most companies.

**Deep dive:** `03-python-tooling/README.md`

## 4. Schema and migrations

*guys this might look boring but is actually very important and will highkey let the interviewers for a jr or even mid level role know that YOU KNOW BALL*

**What it is:** Database schema as code plus numbered migration files.

**Why you need it:** Production data changes safely and predictably with versioned history.

**How often:** 100% of production apps with a database use migrations. The ORM varies (Prisma, Django, Alembic, Flyway) but numbered, versioned migration files are universal.

**Deep dive:** `04-schema-and-migrations/README.md`

5. CI pipeline
**What it is:** Automated checks on every change.
**Why you need it:** You cannot scale review or trust without CI gates.
**How often:** 100% of professional codebases have CI. GitHub Actions is the most common for startups. The path filtering pattern is standard for monorepos.
**Deep dive:** `05-ci-pipeline/README.md`

6. Deployment pipeline
**What it is:** The workflow that turns a merge into a deploy.
**Why you need it:** You need predictable, repeatable, auditable releases.
**How often:** 100% of production apps have a deploy pipeline. The branch-based flow (main to stage to prod) with chained workflows is one of the most common patterns.
**Deep dive:** `06-deployment-pipeline/README.md`

7. Keyless auth (OIDC / WIF)
**What it is:** CI authenticates to cloud without static keys.
**Why you need it:** Static service account keys are a security smell. Short-lived tokens are safer.
**How often:** ~70%+ of teams deploying from CI to cloud use OIDC federation now. It is the modern standard.
**Deep dive:** `07-keyless-auth/README.md`

8. Docker multi-stage builds
**What it is:** Split build stages to keep prod images small.
**Why you need it:** Smaller images are faster, safer, and cheaper to deploy.
**How often:** ~80%+ of containerized apps use multi-stage builds. If you are deploying containers, you need this.
**Deep dive:** `08-docker-multi-stage/README.md`

9. Infrastructure as code
**What it is:** Cloud resources defined in code, not clicks.
**Why you need it:** Reproducibility, reviewability, and no mystery drift.
**How often:** ~80% of production infrastructure is managed as code. Terraform is the most common tool, but Pulumi, CDK, and CloudFormation follow the same principles.
**Deep dive:** `09-infrastructure-as-code/README.md`

**How These Pieces Fit Together**
You clone the repo and run `mise install` to get the right tools. `docker-compose up` gives you the same local dependencies prod uses. You write code and push a branch. CI runs path filtered tests against a real Postgres. When you merge to main, a chained workflow deploys to staging, running migrations first and then shipping code. When you are ready, you merge to prod for a production deploy. All of it uses OIDC so no static keys leak. The deploy ships a slim multi-stage Docker image onto infrastructure defined in Terraform.

**Summary Table**
| Pattern | This Codebase / Applies Everywhere |
| --- | --- |
| Docker Compose | Local dependencies in containers, mirrors prod |
| mise | Tool version pinning and task runner |
| uv + ruff + ty | Fast, strict Python tooling gate |
| Schema and migrations | Numbered migrations, schema as code |
| CI pipeline | Path-filtered tests, service containers |
| Deployment pipeline | Chained deploys, migrations before code |
| Keyless auth | OIDC federation, no static keys |
| Docker multi-stage | Small, secure production images |
| Infrastructure as code | Terraform modules, reproducible infra |

its important to understand that UI frameworks like react, nextjs, etc will change every 3 years but these infra patterns won't
