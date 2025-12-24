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

---

## 5. Cisco Live - High-Scale Event Platform

### Main Architecture
![Cisco Live Platform - 85K RPS](images/05-cisco-main.png)

### Auto-Scaling Architecture
![Auto-Scaling Architecture](images/05-cisco-scaling.png)

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
