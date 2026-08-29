# DevOps E-Commerce Project Summary

A concise breakdown of the DevOps workflow, architecture, tool interactions, and infrastructure rationale implemented across 5 core phases.

---

## 🚀 Architecture Overview
- **Backend Service:** FastAPI (Python 3.12)
- **Database:** PostgreSQL 16 with SQLAlchemy ORM & Alembic Migrations
- **Containerization:** Docker & Docker Compose
- **Testing:** Pytest & HTTPX (Unit, Integration & Boundary testing)
- **CI/CD:** GitHub Actions & GitHub Container Registry (GHCR)
- **Cloud & Deployment:** AWS EC2 with Self-Hosted Runner (Automated CD)
- **Observability:** Grafana Cloud, Grafana Alloy, Prometheus (Metrics), Loki (Logs)
Added small demo on IaC with Terraform and Ansible

Note: There are some errors in the making of this and all will be commented in each commits.
---

## 1. Phase 1 — Git & Docker Fundamentals

### Tool Flow & Interaction
```
Developer Host
│
├── [ Git ] ──────────────► Local Repository (Commits, Diffs, Rollbacks)
│
└── [ Docker Engine ]
          │
          ├── Builds ─────► Docker Image (devops-ecommerce-api:1.0)
          │
          └── Runs ───────► Docker Container (ecommerce-api)
                                  │
                                  ├── Network: ecommerce-net (Bridge)
                                  ├── Storage: ecommerce-db-data (Volume)
                                  └── Port: 8000:8000 (Host ◄──► Container)
```

### Rationale & Objectives
Starting with basic containerization and version control ensures local development parity and prevents "works on my machine" dependency conflicts. Creating dedicated bridge networks and named volumes establishes isolated inter-container communication and guarantees data persistence across container recreations. Practicing intentional rollback strategies via Git simulates real-world production incident response workflows.

---

## 2. Phase 2 — Docker Compose & Database Integration

### Stack Architecture
```
dvops-ecom_default (Docker Network)
                                  │
         ┌────────────────────────┴────────────────────────┐
         ▼                                                 ▼
┌──────────────────┐       SQLAlchemy (ORM)        ┌──────────────────┐
│  ecommerce-api   │ ────────────────────────────► │ecommerce-postgres│
│  (FastAPI:8000)  │        psycopg2 driver        │ (PostgreSQL:5432)│
└────────┬─────────┘                               └────────┬─────────┘
         │                                                  │
         │ Port 8000:8000                                   │
         ▼                                                  ▼
┌──────────────────┐                               ┌──────────────────┐
│   Host / User    │                               │ecommerce-db-data │
│  (Client Access) │                               │ (Docker Volume)  │
└──────────────────┘                               └──────────────────┘
```

### Rationale & Objectives
Manually managing individual containers quickly becomes unmaintainable as application dependencies grow. Introducing Docker Compose centralizes multi-container configurations—linking the API to a persistent PostgreSQL database—into a single declarative stack. Implementing dynamic database drivers, SQLAlchemy ORM, and full CRUD operations shifts the API from static in-memory responses to production-grade persistent data handling.

---

## 3. Phase 3 — Production-Ready Testing & Database Migrations

### Test & Migration Architecture
```
[ models.py ] ──────────► [ Alembic Migrations ] ──────────► [ PostgreSQL ]
                                  │                                ▲
                          Tracks & Versions                        │
                            Schema State                           │
                                  │                                │
[ pytest Suite ] ─────────────────┴────────────────────────────────┤
      │                                                            │
      ├── Positive Tests (Valid CRUD)                              │
      ├── Negative Tests (Invalid types / 404s)                    │
      ├── Boundary Tests (Price > 0 validation)                    │
      │                                                            │
      └── [ conftest.py ]                                          │
               │                                                   │
               ├── Auto-applies: alembic upgrade head ─────────────┤
               └── Manages test DB isolation & cleanup ────────────┘
```

### Rationale & Objectives
Direct application modifications to live databases risk data loss and inconsistent schema states across environments. Integrating Alembic tracks schema changes systematically alongside source code, while container health checks ensure the API waits for database availability before starting. Comprehensive test suites with isolated database fixtures protect core business logic by catching invalid inputs, edge cases, and breaking schema changes before release.

---

## 4. Phase 4 — CI/CD Pipeline & AWS Deployment

### End-to-End Pipeline
```
Developer ──► git push (main / feature/**)
                  │
                  ▼
          [ GitHub Actions CI ]
                  │
                  ├── Spin up ephemeral PostgreSQL 16 service
                  ├── Run Alembic migrations (upgrade head)
                  └── Execute pytest suite
                  │
                  ▼ (If CI Passes on main)
          [ GitHub Actions CD ]
                  │
                  ├── Build multi-tag Docker image (SHA & latest)
                  └── Push Image ──► [ GitHub Container Registry (GHCR) ]
                                                   │
                                            Trigger Deployment
                                                   │
                                                   ▼
                                       [ AWS EC2 Instance ]
                                       (Self-Hosted Runner Service)
                                                   │
                                                   ├── docker compose pull
                                                   ├── docker compose up -d
                                                   └── docker image prune -f
```

### Rationale & Objectives
Manual testing and deployment workflows are error-prone, slow down delivery cycles, and introduce environment drift. Automating Continuous Integration validates code quality through automated test runs against clean ephemeral databases on every push. Extending this with a self-hosted Continuous Delivery runner on AWS EC2 eliminates manual SSH deployments by pulling pre-built container packages directly from GHCR upon approved commits.

---

## 5. Phase 5 — Observability & Monitoring

### Telemetry Pipeline
```
           AWS EC2 Instance
┌──────────────────────────────────────────┐
│                                          │
│  [ Docker Daemon ]                       │
│         │                                │
│         ├── API Container                │
│         └── Postgres Container           │
│                 │                        │
│                 ▼ (Logs)                 │
│         [ /var/run/docker.sock ]         │
│                 │                        │
│                 ▼                        │
│         [ Grafana Alloy ]                │
│         (Collector Daemon)               │
│           │            │                 │
│   (Host Metrics)    (Container Logs)     │
└───────────┼────────────┼─────────────────┘
│            │
▼            ▼
┌──────────────────────────────────────────┐
│              Grafana Cloud               │
│                                          │
│   [ Prometheus ]        [ Loki ]         │
│   (System Metrics)      (Log Aggregation)│
│          │                 │             │
│          └────────┬────────┘             │
│                   ▼                      │
│          [ Grafana Dashboard ]           │
│         (Real-time Observability)        │
└──────────────────────────────────────────┘
```

### Rationale & Objectives
Deploying workloads without real-time monitoring leaves operators blind to system degradation, resource exhaustion, and runtime errors. Implementing Grafana Alloy on the EC2 host creates an automated pipeline that ships host metrics to Prometheus and container runtime logs to Loki. Consolidating these streams into live Grafana dashboards provides visibility into service health, latency, and operational performance.

---

## 🔮 Upcoming Milestones
- **Phase 6:** Kubernetes (K8s) Cluster Deployment (Pods, Services, Ingress, HPA, Probes).
- **Phase 7:** Infrastructure as Code (IaC) using Terraform & Ansible.
- **Phase 8:** DevSecOps security scanning (Trivy container scanning, SBOM, and dependency vulnerability checks).
