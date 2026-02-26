# Keyless Auth (OIDC / WIF)

**The Problem**
Static service account keys are long-lived secrets that leak. They get copied into CI, copied into laptops, and eventually end up in logs or third-party tools. Once leaked, they are valid until you find them and rotate them.

> When Yanjie drives, he ALWAYS puts his vapes in the center console area, in the same place and never changes, when he goes out with vape leechers like Cindy, Emily, Wharton, Michael, and Collin, they realize he always keeps his vapes there so they just help themselves without asking and sometimes even steals them and takes them. Sometimes they just keep fucking asking him for vapes over and over again every few minutes.

> With OIDC and WIF, Yanjie now keeps his vapes in his pockets whenever he's with these people. So when he needs to take a hit, he reaches into his pocket to pull it out and take a hit, this way the time the vape can be taken by them is 'short lived' and since its in his pockets, only he can access his own vape, and these other people can only hit it when he allows them to.

**The Solution**
Use OIDC federation. GitHub generates a short-lived JWT at job runtime. The cloud provider validates it and issues a short-lived access token. No static keys ever exist.

**Real Code**
Here is a GitHub Actions snippet that uses OIDC with Google Cloud. Every non-obvious line is annotated.

```yaml
permissions:
  id-token: write # Required for GitHub to mint an OIDC token.
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - id: auth
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/gha/providers/gha
          service_account: deployer-stage@example-stage.iam.gserviceaccount.com

      - name: Deploy
        run: ./scripts/deploy --env=stage
```

**Step By Step Token Exchange**
1. GitHub creates a short-lived OIDC JWT for the job because `id-token: write` is enabled.
2. The action sends that JWT to the cloud provider's identity endpoint.
3. The provider validates the JWT against the configured workload identity pool.
4. The provider issues a short-lived access token scoped to the service account.
5. The job uses that token to deploy. No static keys ever touch disk.

**Key Lessons**
- Static keys are a security smell. If you see one, replace it.
- OIDC federation makes tokens short-lived and tied to a specific workflow.
- Isolate environments. Dev, stage, and prod should be separate projects and service accounts.

**How This Applies Elsewhere**
AWS supports OIDC with IAM roles for GitHub Actions. Azure supports Federated Credentials for service principals. The idea is identical: trust the CI identity, issue short-lived tokens, never store keys.
