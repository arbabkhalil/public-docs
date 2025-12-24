# Enterprise Kubernetes Migration - HCL Commerce Platform

## Project Overview

**Client:** Parker Hannifin (via Redify s.r.l)  
**Location:** Bologna, Italy (Remote)  
**Duration:** February 2024 - September 2024  
**Role:** Consultant DevOps Engineer (Freelance)

---

## Executive Summary

Led the complex migration of Parker Hannifin's HCL Commerce platform from legacy VM-based deployment (v8) to modern Kubernetes-based architecture (v9) on Azure AKS. Developed custom ArgoCD plugins and advanced Kustomize overlays to handle enterprise-specific requirements while maintaining compatibility with vendor-provided Helm charts.

---

## Business Challenge

Parker Hannifin, a Fortune 250 company, needed to modernize their e-commerce infrastructure:

- **Legacy VM architecture** - HCL Commerce v8 running on traditional VMs
- **Scaling limitations** - Manual scaling, slow deployments
- **Vendor lock-in** - Community Helm charts couldn't be modified directly
- **Multiple environments** - Need to manage dev, staging, UAT, and production
- **Zero downtime requirement** - Critical e-commerce platform serving global customers
- **Secret management** - Enterprise-grade security requirements

---

## Solution Architecture

### Architecture Diagrams

![HCL Commerce Platform Architecture](diagrams/images/03-hcl-main.png)

![Blue-Green Deployment Strategy](diagrams/images/03-hcl-bluegreen.png)

---

## Technical Implementation

### 1. Custom ArgoCD Plugin for Kustomize + Helm

The challenge: HCL Commerce provides Helm charts that couldn't be modified, but Parker needed environment-specific customizations.

**Solution: Custom ArgoCD Config Management Plugin**

```yaml
# argocd-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-cm
data:
  configManagementPlugins: |
    - name: kustomize-helm
      init:
        command: ["/bin/sh", "-c"]
        args:
          - |
            helm dependency build charts/hcl-commerce || true
      generate:
        command: ["/bin/sh", "-c"]
        args:
          - |
            helm template $ARGOCD_APP_NAME charts/hcl-commerce \
              -f values/$ENV/values.yaml \
              --include-crds | \
            kustomize build overlays/$ENV
```

**Plugin Workflow:**

The custom ArgoCD plugin layers Kustomize customizations on top of vendor Helm charts without modification.

### 2. Multi-Environment Configuration with SOPS

**Repository Structure:**
```
hcl-commerce-deployment/
├── charts/
│   └── hcl-commerce/           # Vendor Helm chart (submodule)
├── overlays/
│   ├── dev/
│   │   ├── kustomization.yaml
│   │   └── patches/
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   └── patches/
│   └── production/
│       ├── kustomization.yaml
│       └── patches/
├── values/
│   ├── dev/
│   │   ├── values.yaml
│   │   └── secrets.enc.yaml    # SOPS encrypted
│   ├── staging/
│   │   ├── values.yaml
│   │   └── secrets.enc.yaml
│   └── production/
│       ├── values.yaml
│       └── secrets.enc.yaml
└── argocd/
    └── applications/
```

**SOPS Integration with ArgoCD:**
```yaml
# Kustomize secretGenerator with SOPS
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - ../../base
secretGenerator:
  - name: hcl-commerce-secrets
    files:
      - secrets.enc.yaml
generatorOptions:
  disableNameSuffixHash: true
```

### 3. Blue-Green Deployments with Argo Rollouts

**Dynamic Deployment to Rollout Conversion:**

```yaml
# Kustomize patch to convert Deployment to Rollout
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: store-server
spec:
  strategy:
    blueGreen:
      activeService: store-server-active
      previewService: store-server-preview
      autoPromotionEnabled: false
      scaleDownDelaySeconds: 30
```

The blue-green deployment strategy is illustrated in the architecture diagrams above.

### 4. Azure DevOps Pipeline

```yaml
# azure-pipelines.yaml
trigger:
  branches:
    include:
      - main
      - release/*

stages:
  - stage: Build
    jobs:
      - job: BuildImages
        steps:
          - task: Docker@2
            inputs:
              command: buildAndPush
              repository: hcl-commerce-custom
              
  - stage: DeployDev
    dependsOn: Build
    jobs:
      - job: SyncArgoCD
        steps:
          - script: |
              argocd app sync hcl-commerce-dev
              argocd app wait hcl-commerce-dev
              
  - stage: DeployStaging
    dependsOn: DeployDev
    jobs:
      - job: SyncArgoCD
        steps:
          - script: |
              argocd app sync hcl-commerce-staging
              
  - stage: DeployProduction
    dependsOn: DeployStaging
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: Production
        environment: production
        strategy:
          runOnce:
            deploy:
              steps:
                - script: |
                    argocd app sync hcl-commerce-prod
```

---

## Key Achievements

| Metric | Before (v8 VM) | After (v9 K8s) | Improvement |
|--------|----------------|----------------|-------------|
| Deployment Time | 4-6 hours | 15-30 minutes | **90% faster** |
| Rollback Time | 2-4 hours | < 2 minutes | **99% faster** |
| Scaling Time | 30+ minutes | 2-3 minutes | **90% faster** |
| Environment Parity | Poor | Identical | **100% consistent** |
| Secret Management | Manual | Automated (SOPS) | **Fully automated** |
| Downtime per Deploy | 30-60 minutes | Zero | **100% reduction** |

---

## Technologies Used

**Cloud Platform:**
- Microsoft Azure (AKS, SQL, Blob Storage, Redis Cache)
- Azure DevOps (Pipelines, Repos)

**Kubernetes & Containers:**
- Azure Kubernetes Service (AKS)
- Helm, Kustomize
- ArgoCD (with custom plugin)
- Argo Rollouts

**Security & Secrets:**
- SOPS (Secrets OPerationS)
- Azure Key Vault
- Workload Identity

**Application:**
- HCL Commerce v9
- Apache NiFi
- Elasticsearch

---

## Unique Challenges Solved

### 1. Vendor Chart Compatibility
Created custom ArgoCD plugin to layer Kustomize on top of vendor Helm charts without modifying them.

### 2. Multi-Values Files
Designed SOPS integration supporting multiple values files per environment (base + secrets).

### 3. Zero-Downtime Migration
Implemented phased migration strategy with parallel VM and K8s environments during transition.

### 4. Enterprise Compliance
Met enterprise security requirements with encrypted secrets, RBAC, and audit logging.

---

## Sample Deliverables

1. **Custom ArgoCD Plugin** - Kustomize + Helm integration
2. **Kustomize Overlays** - Environment-specific configurations
3. **SOPS Configuration** - Encrypted secrets management
4. **Argo Rollouts Configs** - Blue-Green deployment strategies
5. **Azure DevOps Pipelines** - Complete CI/CD workflow
6. **Migration Runbooks** - Step-by-step migration documentation

---

## Contact

**Available for similar projects involving:**
- Kubernetes migrations from VM-based systems
- HCL Commerce or enterprise e-commerce platforms
- Custom ArgoCD plugin development
- Advanced Kustomize and Helm configurations
- Blue-Green and Canary deployment strategies
- Azure AKS implementation
