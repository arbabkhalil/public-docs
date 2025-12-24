# Architecture Diagrams - Professional Cloud Icons

These diagrams were generated using the [diagrams](https://diagrams.mingrammer.com/) Python library with **official cloud provider icons** from AWS, Azure, GCP, and Kubernetes.

---

## 1. Internal Developer Platform (AERQ)

### Main Architecture
![Internal Developer Platform](images/01-idp-main.png)

### GitOps Workflow
![GitOps Workflow](images/01-idp-gitops.png)

---

## 2. Hybrid Edge-Cloud Architecture (ChaiOne TMS)

### Main Architecture
![Hybrid Edge-Cloud Architecture](images/02-edge-cloud-main.png)

### Edge Device Architecture
![Edge Device Architecture](images/02-edge-device.png)

### CI/CD Pipeline
![CI/CD Pipeline](images/02-cicd-pipeline.png)

---

## 3. HCL Commerce Kubernetes Migration (Parker/Redify)

### Main Architecture
![HCL Commerce on AKS](images/03-hcl-main.png)

### Blue-Green Deployment
![Blue-Green Deployment](images/03-hcl-bluegreen.png)

---

## 4. edX Platform - SRE Architecture

### Main Architecture
![edX Platform Architecture](images/04-edx-main.png)

### Migration Flow
![EC2 to EKS Migration](images/04-edx-migration.png)

### Incident Response
![Incident Response Flow](images/04-incident-response.png)

---

## 5. Cisco Live - High-Scale Event Platform

### Main Architecture
![Cisco Live Platform - 85K RPS](images/05-cisco-main.png)

### Auto-Scaling Architecture
![Auto-Scaling Architecture](images/05-cisco-scaling.png)

---

## All Diagrams (12 Total)

| # | File | Description |
|---|------|-------------|
| 1 | `01-idp-main.png` | Internal Developer Platform - Azure AKS |
| 2 | `01-idp-gitops.png` | GitOps Workflow with ArgoCD |
| 3 | `02-edge-cloud-main.png` | Hybrid Edge-Cloud TMS Architecture |
| 4 | `02-edge-device.png` | Edge Device Stack (Docker/IoT) |
| 5 | `02-cicd-pipeline.png` | CI/CD Pipeline for Edge Deployment |
| 6 | `03-hcl-main.png` | HCL Commerce on AKS |
| 7 | `03-hcl-bluegreen.png` | Blue-Green Deployment Strategy |
| 8 | `04-edx-main.png` | edX Platform AWS Architecture |
| 9 | `04-edx-migration.png` | EC2 to EKS Migration Path |
| 10 | `04-incident-response.png` | SRE Incident Response Flow |
| 11 | `05-cisco-main.png` | Cisco Live 85K RPS Platform |
| 12 | `05-cisco-scaling.png` | GCP Auto-Scaling Architecture |

---

## Regenerating Diagrams

To regenerate or modify these diagrams, run:

```bash
cd /Users/arbab.khalil/personal/public-docs/upwork-portfolios/diagrams
python generate_diagrams.py
```

### Requirements
- Python 3.8+
- `pip install diagrams`
- Graphviz (`brew install graphviz` on macOS)

### Customization
Edit `generate_diagrams.py` to:
- Add new components
- Change colors/themes
- Modify layout direction
- Add more cloud services
