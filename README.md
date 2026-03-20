# 🚀 DevOps Lab – End-to-End Local Platform

Et komplett lokalt DevOps-prosjekt som demonstrerer:

* Docker containerisering
* Kubernetes (Docker Desktop)
* Helm charts
* ArgoCD (GitOps)
* CI/CD med GitHub Actions
* Prometheus + Grafana monitoring

Målet er læring gjennom en realistisk, men enkel arkitektur.

---

# 🧱 Arkitektur

```
Developer → GitHub → GitHub Actions (CI/CD)
                     ↓
                DockerHub (image)
                     ↓
                Git (Helm values update)
                     ↓
                 ArgoCD (GitOps)
                     ↓
               Kubernetes Cluster
                     ↓
        Prometheus → Grafana Dashboard
```

---

# 📦 Fase 1 – Application + Container

## App

En liten FastAPI-applikasjon med:

* `/healthz` – health check
* `/greet` – business logic
* `/metrics` – Prometheus metrics
* Environment-based config
* Modulstruktur (ikke single-file)

### Struktur

```
app/
  main.py
  routes.py
  service.py
  config.py
tests/
Dockerfile
requirements.txt
```

## Lokal kjøring

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Test:

```bash
curl http://localhost:8000/healthz
curl http://localhost:8000/greet
curl http://localhost:8000/metrics
```

---

## Docker

Bygg image:

```bash
docker build -t <dockerhub-user>/devops-lab:1.0 .
```

Kjør container:

```bash
docker run -p 8000:8000 <dockerhub-user>/devops-lab:1.0
```

Push til DockerHub:

```bash
docker push <dockerhub-user>/devops-lab:1.0
```

---

# ☸️ Fase 2 – Kubernetes + Helm + ArgoCD

## Namespaces

```
app-dev
app-prod
argocd
monitor
```

---

## Helm Chart

Plassering:

```
deploy/charts/devops-lab/
```

Inneholder:

* Deployment
* Service
* ConfigMap
* HPA (optional via values)
* values.yaml
* values-dev.yaml
* values-prod.yaml

### Installasjon manuelt

Dev:

```bash
helm upgrade --install app-dev ./deploy/charts/devops-lab \
  -n app-dev \
  -f deploy/charts/devops-lab/values-dev.yaml
```

Prod:

```bash
helm upgrade --install app-prod ./deploy/charts/devops-lab \
  -n app-prod \
  -f deploy/charts/devops-lab/values-prod.yaml
```

---

## ArgoCD (GitOps)

Installeres i namespace `argocd`.

ArgoCD Applications:

```
deploy/argocd/app-dev.yaml
deploy/argocd/app-prod.yaml
```

ArgoCD:

* Leser Helm chart fra Git
* Bruker riktig values-fil per miljø
* Auto-sync aktivert
* Git er "source of truth"

Ingen `kubectl apply` i pipeline.

---

# 🔁 Fase 3 – Monitoring

Installeres i namespace `monitor`.

## kube-prometheus-stack

Installeres via Helm:

```bash
helm upgrade --install kps prometheus-community/kube-prometheus-stack \
  -n monitor \
  -f deploy/monitor/kps-values.yaml
```

Inneholder:

* Prometheus
* Grafana
* Prometheus Operator
* Alertmanager

---

## ServiceMonitor

For hvert miljø:

```
deploy/monitor/servicemonitor-app-dev.yaml
deploy/monitor/servicemonitor-app-prod.yaml
```

Disse forteller Prometheus å scrape `/metrics`.

---

## Grafana Dashboard

Provisioneres via ConfigMap:

```
deploy/monitor/grafana-dashboard-devops-lab.yaml
```

Viser:

* `app_requests_total`
* Requests per path
* Rate over tid

---

# 🔄 CI/CD Pipeline

Ligger i:

```
.github/workflows/
```

## CI

* Kjører tester
* Bygger Docker image

## CD Dev (automatisk)

Ved push til main/master:

1. Build image
2. Push til DockerHub (tag = commit SHA)
3. Oppdater `values-dev.yaml`
4. Commit tilbake til repo
5. ArgoCD deployer automatisk

## CD Prod (manuell)

Manuell trigger:

1. Oppdater `values-prod.yaml` med valgt image tag
2. Commit til Git
3. ArgoCD deployer prod

---

# 🔐 GitHub Secrets

Repository secrets:

```
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
```

Bruk DockerHub Access Token (ikke passord).

---

# 🧠 Hva dette prosjektet lærer deg

### Docker

* Multi-layer builds
* Non-root container
* Environment config
* Image versioning

### Kubernetes

* Deployment vs Service
* Readiness & liveness probes
* Namespaces
* HPA
* Resource requests/limits

### Helm

* Templating
* values.yaml per miljø
* Reusable chart design

### ArgoCD

* GitOps workflow
* Declarative Applications
* Auto sync
* Drift correction

### CI/CD

* GitHub Actions
* SHA-based image tagging
* Automated Git updates
* Environment promotion

### Observability

* Prometheus scraping
* ServiceMonitor
* Grafana dashboards
* Metrics-based verification

---

# 🧪 End-to-End Test

Push en kodeendring.

Du skal se:

1. GitHub Action kjører
2. Image pushes til DockerHub
3. values-dev.yaml oppdateres
4. ArgoCD synker
5. Kubernetes ruller ut ny pod
6. Grafana viser økt request-rate

Hvis alle disse skjer:

Du har bygget en komplett DevOps pipeline.

---

# 🛠️ Vanlige Problemer

### ImagePullBackOff

Feil DockerHub repo/tag eller privat repo uten credentials.

### ArgoCD OutOfSync

Feil branch eller path i Application YAML.

### HPA virker ikke

Metrics Server mangler i cluster.

### Prometheus target = DOWN

ServiceMonitor selector matcher ikke Service labels.

---



# 🏁 Oppsummering

Dette prosjektet implementerer en realistisk DevOps-plattform lokalt:

* Containerized app
* Kubernetes miljøer
* Helm-based deploy
* GitOps via ArgoCD
* CI/CD pipeline
* Full monitoring stack

Alt kjører lokalt, uten cloud-spesifikke tjenester.

