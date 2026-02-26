# Infrastructure As Code

**The Problem**
Clicking through cloud consoles is not reproducible. Nobody remembers what they clicked, drift accumulates, and you cannot review or roll back infra changes. That is how outages happen.

> Audrey and Iana are trying to work together to get a marketing video out for Gen AI and are getting the new members to film it. They verbally tell the new members to make sure the video is filmed on the Glade, and not to enter the library and cause a disturbance, and if they do, don't say they're from Gen AI.

> They forget and say they're from gen ai and make irreversable pr damages..

> Audrey and Iana terraforms this down to every single specifics so the new members will follow the video instructions perfectly.

> Now that the new members have this specific rule in hand, they can practice in any environment from scratch, do this in real life, and follow every single instruction repeatedly so the video stays consistent and the same everytime they film again.

**The Solution**
Define infrastructure as code. Terraform lets you describe networks, services, and IAM in a reviewable, repeatable way. You can run it in CI, you can review it in PRs, and you can recreate the entire environment from scratch.

**Real Code**
Below are Terraform snippets that show the core patterns: VPC networking, a serverless connector, reusable modules, and BigQuery federation.

```hcl
# vpc.tf
resource "google_compute_network" "main" {
  name                    = "example-vpc"
  auto_create_subnetworks = false # Keep subnets explicit and intentional.
}

resource "google_compute_subnetwork" "private" {
  name          = "example-private"
  ip_cidr_range = "10.10.0.0/16"
  region        = var.region
  network       = google_compute_network.main.id
}

resource "google_vpc_access_connector" "serverless" {
  name          = "serverless-connector"
  region        = var.region
  ip_cidr_range = "10.8.0.0/28" # Small range dedicated to serverless.
  network       = google_compute_network.main.name
}
```

```hcl
# modules/service/main.tf
resource "google_cloud_run_service" "app" {
  name     = var.name
  location = var.region

  template {
    spec {
      containers {
        image = var.image
      }
    }
  }

  metadata {
    annotations = {
      "run.googleapis.com/vpc-access-connector" = var.vpc_connector
      "run.googleapis.com/vpc-access-egress"    = "all-traffic" # Force private egress.
    }
  }
}
```

```hcl
# envs/stage/main.tf
module "api" {
  source        = "../../modules/service"
  name          = "api"
  region        = var.region
  image         = var.api_image
  vpc_connector = google_vpc_access_connector.serverless.id
}

module "worker" {
  source        = "../../modules/service"
  name          = "worker"
  region        = var.region
  image         = var.worker_image
  vpc_connector = google_vpc_access_connector.serverless.id
}
```

```hcl
# bigquery.tf
resource "google_bigquery_connection" "cloudsql" {
  connection_id = "cloudsql-conn"
  location      = var.region
  cloud_sql {
    instance_id = var.cloudsql_instance
    database    = "app"
    type        = "POSTGRES"
    credential {
      username = var.cloudsql_user
      password = var.cloudsql_password
    }
  }
}
```

**Key Lessons**
- Infra changes should be reviewed like code.
- VPCs and connectors let serverless services reach private resources safely.
- Modules keep infra DRY. One service module, many instantiations.
- BigQuery federation gives the data team access without copying data everywhere.

**How This Applies Elsewhere**
Terraform is common, but Pulumi, CDK, and CloudFormation are all the same idea: infrastructure as code, reviewed, versioned, and reproducible.
