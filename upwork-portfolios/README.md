# Upwork Portfolio Collection

This folder contains detailed portfolio documents and architecture diagrams for Upwork profiles.

## 📁 Structure

```
upwork-portfolios/
├── README.md                                    # This file
├── 01-internal-developer-platform.md            # AERQ - IDP Project
├── 02-hybrid-edge-cloud-architecture.md         # ChaiOne - TMS Project
├── 03-enterprise-kubernetes-migration.md        # Parker/Redify - HCL Commerce
├── 04-high-scale-sre-edx.md                     # edX - SRE Project
├── 05-cisco-live-high-scale-event.md            # Cisco Live - Event Platform
├── upwork-profile-descriptions.md               # Copy-paste ready profile content
└── diagrams/
    ├── generate_diagrams.py                     # Python script to regenerate diagrams
    ├── README.md                                # Diagram index with previews
    └── images/                                  # Generated PNG diagrams
        ├── 01-idp-main.png                      # IDP Main Architecture
        ├── 01-idp-gitops.png                    # IDP GitOps Workflow
        ├── 02-edge-cloud-main.png               # Edge-Cloud Architecture
        ├── 03-hcl-main.png                      # HCL Commerce Platform
        ├── 03-hcl-bluegreen.png                 # Blue-Green Deployment
        ├── 04-edx-main.png                      # edX Platform Architecture
        ├── 04-edx-migration.png                 # EC2 to EKS Migration
        ├── 05-cisco-main.png                    # Cisco Live Architecture
        └── 05-cisco-scaling.png                 # Auto-Scaling Architecture
```

---

## 🎯 Two Upwork Profiles

### Profile 1: DevOps & Platform Engineering Specialist

**Best for:** Startups, SaaS companies, companies adopting Kubernetes

**Highlighted Projects:**
1. [Internal Developer Platform (AERQ)](01-internal-developer-platform.md)
2. [Hybrid Edge-Cloud Architecture (ChaiOne)](02-hybrid-edge-cloud-architecture.md)
3. [Enterprise Kubernetes Migration (Parker)](03-enterprise-kubernetes-migration.md)

**Suggested Rate:** $80-120/hr

---

### Profile 2: Cloud Architect & SRE Specialist

**Best for:** Enterprise, high-scale systems, regulated industries

**Highlighted Projects:**
1. [High-Scale SRE at edX](04-high-scale-sre-edx.md)
2. [Cisco Live Event Platform](05-cisco-live-high-scale-event.md)
3. [Enterprise Kubernetes Migration (Parker)](03-enterprise-kubernetes-migration.md)

**Suggested Rate:** $100-150/hr

---

## 📊 Architecture Diagrams

All diagrams are generated using Python with the `diagrams` library, featuring **official AWS, Azure, GCP, and Kubernetes icons**.

### Pre-generated PNG Images

The `diagrams/images/` folder contains ready-to-use PNG files:

| Diagram | Description |
|---------|-------------|
| `01-idp-main.png` | Internal Developer Platform on Azure |
| `01-idp-gitops.png` | GitOps Workflow with ArgoCD |
| `02-edge-cloud-main.png` | Hybrid Edge-Cloud Architecture on AWS |
| `03-hcl-main.png` | HCL Commerce Platform on Azure AKS |
| `03-hcl-bluegreen.png` | Blue-Green Deployment Strategy |
| `04-edx-main.png` | edX Learning Platform on AWS |
| `04-edx-migration.png` | EC2 to EKS Migration Path |
| `05-cisco-main.png` | Cisco Live Platform on GCP |
| `05-cisco-scaling.png` | Auto-Scaling Architecture |

### Regenerating Diagrams

To regenerate the diagrams (requires Python and Graphviz):

```bash
# Install dependencies
pip install diagrams
brew install graphviz  # macOS

# Generate diagrams
cd upwork-portfolios/diagrams
python generate_diagrams.py
```

---

## 📄 Creating PDFs for Upload

### Using VS Code:
1. Install "Markdown PDF" extension
2. Open any .md file
3. Press `Cmd+Shift+P` → "Markdown PDF: Export (pdf)"

### Using Pandoc:
```bash
pandoc 01-internal-developer-platform.md -o portfolio-idp.pdf
```

### Using Online Tools:
1. [StackEdit](https://stackedit.io/) - Paste markdown, export PDF
2. [Dillinger](https://dillinger.io/) - Markdown editor with export

---

## 🔗 Upwork Portfolio Upload Tips

1. **PDF Format** - Convert markdown to PDF for cleaner presentation
2. **Include Diagrams** - Export Mermaid diagrams as images, embed in PDF
3. **One Project Per Portfolio Item** - Don't combine multiple projects
4. **Add Cover Image** - Use architecture diagram as cover
5. **Keep Description Short** - Link to full PDF in description

---

## 📝 Quick Portfolio Descriptions (Copy-Paste for Upwork)

### Internal Developer Platform
> Designed and implemented an Internal Developer Platform (IDP) using Kubernetes (AKS), ArgoCD, Terraform, and HashiCorp Vault. Transformed DevOps team into Platform Engineering, reducing deployment time by 98% and new engineer onboarding from 3 weeks to 3 days.

### Hybrid Edge-Cloud Architecture
> Architected a hybrid edge-cloud deployment for Terminal Management System. Implemented K3s on CoreOS edge devices connected via site-to-site VPN to AWS EKS. Enabled offline-first operations with automatic cloud sync when connectivity is restored.

### HCL Commerce Kubernetes Migration
> Led migration of enterprise HCL Commerce platform from VMs to Kubernetes (AKS). Developed custom ArgoCD plugin for Helm + Kustomize integration. Implemented Blue-Green deployments with Argo Rollouts, achieving zero-downtime deployments.

### edX SRE
> Site Reliability Engineer for one of the world's largest online learning platforms. Managed AWS infrastructure for 50+ microservices serving 50M+ learners. Led migrations from EC2 to EKS and implemented GitOps with ArgoCD.

### Cisco Live Event Platform
> Architected infrastructure for Cisco Live global event handling 85,000+ requests/second at peak. Deployed auto-scaling platform with 150 application nodes and 32 database nodes on GCP. Achieved 100% uptime during 3-day event.

---

## ✅ Checklist Before Uploading

- [ ] Convert to PDF with proper formatting
- [ ] Export architecture diagrams as images (PNG/SVG)
- [ ] Redact any sensitive client information
- [ ] Add portfolio cover image
- [ ] Write short Upwork description (use templates above)
- [ ] Set appropriate skills tags
- [ ] Link to full documentation if available
