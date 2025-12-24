# HCL Commerce Kubernetes Migration - Diagram

## Mermaid Diagram - Overall Architecture

```mermaid
flowchart TB
    subgraph "Azure Cloud"
        subgraph "Azure Kubernetes Service"
            subgraph "HCL Commerce v9"
                STORE[Store Server]
                SEARCH[Search Server]
                AUTH[Auth Server]
                TS[Transaction Server]
                XC[XC Server]
                TOOLING[Tooling Server]
                NIFI[NiFi Ingest]
                CACHE[Redis Cache]
            end
            
            subgraph "Platform Services"
                ARGO[ArgoCD + Custom Plugin]
                SOPS[SOPS Secrets]
                ROLLOUTS[Argo Rollouts]
                NGINX[Ingress NGINX]
            end
        end
        
        subgraph "Azure Managed Services"
            SQL[(Azure SQL)]
            BLOB[Azure Blob]
            REDIS[(Azure Redis)]
            KV[Key Vault]
        end
    end

    subgraph "CI/CD"
        ADO[Azure DevOps]
        HELM[Helm Charts]
        KUST[Kustomize Overlays]
    end

    ADO --> ARGO
    HELM --> ARGO
    KUST --> ARGO
    ARGO --> STORE
    ARGO --> SEARCH
    ARGO --> AUTH
    SOPS --> ARGO
    ROLLOUTS --> STORE
    STORE --> SQL
    STORE --> BLOB
    STORE --> REDIS
```

---

## Blue-Green Deployment Flow

```mermaid
flowchart LR
    subgraph "Before Deployment"
        subgraph "Active (Blue)"
            BLUE[v1.0.0<br/>Store Server]
        end
        ACTIVE_SVC[Active Service]
        TRAFFIC1[100% Traffic] --> ACTIVE_SVC --> BLUE
    end
    
    subgraph "During Deployment"
        subgraph "Active (Blue) "
            BLUE2[v1.0.0]
        end
        subgraph "Preview (Green)"
            GREEN[v1.1.0]
        end
        ACTIVE_SVC2[Active Service]
        PREVIEW_SVC[Preview Service]
        TRAFFIC2[Production] --> ACTIVE_SVC2 --> BLUE2
        TEST[QA Testing] --> PREVIEW_SVC --> GREEN
    end
    
    subgraph "After Promotion"
        subgraph "Standby (Blue)  "
            BLUE3[v1.0.0]
        end
        subgraph "Active (Green) "
            GREEN2[v1.1.0]
        end
        ACTIVE_SVC3[Active Service]
        TRAFFIC3[100% Traffic] --> ACTIVE_SVC3 --> GREEN2
    end
```

---

## Custom ArgoCD Plugin Flow

```mermaid
flowchart LR
    subgraph "Git Repository"
        VALUES[values.yaml]
        SECRETS[secrets.enc.yaml]
        OVERLAY[Kustomize Overlay]
        CHART[Vendor Helm Chart]
    end

    subgraph "ArgoCD Custom Plugin"
        STEP1[1. Helm Template]
        STEP2[2. SOPS Decrypt]
        STEP3[3. Kustomize Build]
    end

    subgraph "Output"
        MANIFESTS[Final K8s Manifests]
    end

    CHART --> STEP1
    VALUES --> STEP1
    SECRETS --> STEP2
    STEP1 --> STEP3
    STEP2 --> STEP3
    OVERLAY --> STEP3
    STEP3 --> MANIFESTS
```

---

## PlantUML Diagram

```plantuml
@startuml HCL Commerce Migration Architecture

skinparam backgroundColor #FFFFFF

package "Azure DevOps" {
    [Pipeline] as ADO
    [Helm Charts] as Helm
    [Kustomize] as Kust
}

cloud "Azure Kubernetes Service" {
    package "Platform Layer" {
        [ArgoCD] as Argo
        [Custom Plugin] as Plugin
        [SOPS Secrets] as SOPS
        [Argo Rollouts] as Rollouts
    }
    
    package "HCL Commerce v9" {
        [Store Server] as Store
        [Search Server] as Search
        [Auth Server] as Auth
        [Transaction Server] as TS
        [XC Server] as XC
        [Tooling] as Tool
        [NiFi] as Nifi
    }
    
    package "Supporting" {
        [Redis Cache] as Redis
        [Elasticsearch] as ES
    }
}

package "Azure Managed Services" {
    database "Azure SQL" as SQL
    storage "Blob Storage" as Blob
    [Key Vault] as KV
}

ADO --> Argo
Helm --> Plugin
Kust --> Plugin
Plugin --> Argo
SOPS --> Argo
Argo --> Store
Argo --> Search
Argo --> Auth
Argo --> TS
Rollouts --> Store
Store --> SQL
Store --> Blob
Search --> ES
KV --> SOPS

@enduml
```

---

## Migration Phases Diagram

```mermaid
gantt
    title HCL Commerce v8 to v9 Migration Timeline
    dateFormat  YYYY-MM-DD
    
    section Assessment
    Infrastructure Analysis    :done, a1, 2024-02-01, 2w
    Dependency Mapping         :done, a2, after a1, 1w
    Risk Assessment           :done, a3, after a2, 1w
    
    section Infrastructure Setup
    AKS Cluster Provisioning  :done, b1, 2024-03-01, 2w
    Platform Services Setup   :done, b2, after b1, 2w
    ArgoCD + Plugin           :done, b3, after b2, 2w
    
    section Migration
    Dev Environment           :done, c1, 2024-04-15, 3w
    Staging Environment       :done, c2, after c1, 2w
    UAT Environment           :done, c3, after c2, 2w
    Production Cutover        :done, c4, after c3, 2w
    
    section Optimization
    Performance Tuning        :active, d1, 2024-08-01, 3w
    Documentation             :active, d2, after d1, 2w
```

---

## Environment Configuration Structure

```mermaid
flowchart TB
    subgraph "Repository Structure"
        subgraph "charts/"
            VENDOR[hcl-commerce/]
        end
        
        subgraph "overlays/"
            DEV_OL[dev/]
            STG_OL[staging/]
            PROD_OL[production/]
        end
        
        subgraph "values/"
            DEV_V[dev/values.yaml<br/>dev/secrets.enc.yaml]
            STG_V[staging/values.yaml<br/>staging/secrets.enc.yaml]
            PROD_V[production/values.yaml<br/>production/secrets.enc.yaml]
        end
    end

    subgraph "ArgoCD Applications"
        DEV_APP[hcl-commerce-dev]
        STG_APP[hcl-commerce-staging]
        PROD_APP[hcl-commerce-prod]
    end

    VENDOR --> DEV_APP
    VENDOR --> STG_APP
    VENDOR --> PROD_APP
    DEV_OL --> DEV_APP
    STG_OL --> STG_APP
    PROD_OL --> PROD_APP
    DEV_V --> DEV_APP
    STG_V --> STG_APP
    PROD_V --> PROD_APP
```

---

## Component Descriptions for Design Tools

### AKS Components:
| Component | Purpose | Replicas |
|-----------|---------|----------|
| Store Server | Customer-facing storefront | 3-6 |
| Search Server | Product search (Elasticsearch) | 2-4 |
| Auth Server | Authentication & sessions | 2-3 |
| Transaction Server | Order processing | 2-4 |
| XC Server | Extended catalog | 2 |
| Tooling Server | Admin tools | 1-2 |
| NiFi | Data ingestion | 1-2 |

### Platform Components:
| Component | Purpose |
|-----------|---------|
| ArgoCD | GitOps deployment |
| Custom Plugin | Helm + Kustomize integration |
| SOPS | Encrypted secrets |
| Argo Rollouts | Blue-Green deployments |
| Ingress NGINX | Traffic routing |
