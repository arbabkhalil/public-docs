# edX Platform - SRE Architecture Diagram

## Mermaid Diagram - Overall Architecture

```mermaid
flowchart TB
    subgraph "Users"
        LEARNERS[👥 50M+ Global Learners]
    end

    subgraph "Edge & CDN"
        R53[Route 53 DNS]
        CF[CloudFront CDN]
        WAF[AWS WAF]
    end

    subgraph "Application Tier - EKS"
        subgraph "Core Services"
            LMS[LMS Service]
            CMS[CMS/Studio]
            ECOMM[Ecommerce]
            DISCOVERY[Discovery]
            CREDENTIALS[Credentials]
        end
        
        subgraph "Supporting Services"
            NOTES[Notes]
            FORUMS[Forums]
            ANALYTICS[Analytics]
            GRADING[Grading]
            PLUS40[+40 more...]
        end
    end

    subgraph "Legacy - ASG"
        LEGACY[Legacy EC2 Services<br/>Migration Target]
    end

    subgraph "Data Layer"
        RDS[(RDS MySQL<br/>Multi-AZ)]
        REDIS[(ElastiCache<br/>Redis)]
        ES[(Elasticsearch<br/>50+ nodes)]
        S3[S3 Storage<br/>Petabytes]
    end

    subgraph "GitOps"
        ARGOCD[ArgoCD]
        HELM[Helm Charts]
    end

    subgraph "Observability"
        NR[New Relic APM]
        PD[PagerDuty]
        CW[CloudWatch]
    end

    LEARNERS --> R53 --> CF --> WAF
    WAF --> LMS
    WAF --> CMS
    WAF --> LEGACY
    
    LMS --> RDS
    LMS --> REDIS
    LMS --> ES
    CMS --> S3
    
    ARGOCD --> LMS
    ARGOCD --> CMS
    ARGOCD --> ECOMM
    
    LMS --> NR
    NR --> PD
```

---

## Migration Architecture

```mermaid
flowchart LR
    subgraph "Source: EC2 Auto Scaling"
        EC2[EC2 Instances]
        ASG[Auto Scaling Group]
        AMI[AMI-based Deploy]
    end

    subgraph "Migration Process"
        DOCKER[Containerize]
        HELM[Create Helm Chart]
        TEST[Parallel Testing]
        TRAFFIC[Traffic Shift]
    end

    subgraph "Target: EKS"
        EKS[EKS Cluster]
        PODS[Kubernetes Pods]
        ARGO[ArgoCD Deploy]
    end

    EC2 --> DOCKER
    ASG --> DOCKER
    DOCKER --> HELM
    HELM --> TEST
    TEST --> TRAFFIC
    TRAFFIC --> EKS
    EKS --> PODS
    ARGO --> PODS
```

---

## Traffic Shifting Strategy

```mermaid
flowchart TB
    subgraph "Phase 1: 10%"
        P1_EC2[EC2: 90%]
        P1_EKS[EKS: 10%]
    end
    
    subgraph "Phase 2: 50%"
        P2_EC2[EC2: 50%]
        P2_EKS[EKS: 50%]
    end
    
    subgraph "Phase 3: 90%"
        P3_EC2[EC2: 10%]
        P3_EKS[EKS: 90%]
    end
    
    subgraph "Phase 4: Complete"
        P4_EKS[EKS: 100%]
        DECOM[EC2 Decommission]
    end

    P1_EC2 --> P2_EC2 --> P3_EC2 --> DECOM
    P1_EKS --> P2_EKS --> P3_EKS --> P4_EKS

    style P1_EKS fill:#90EE90
    style P2_EKS fill:#90EE90
    style P3_EKS fill:#90EE90
    style P4_EKS fill:#90EE90
```

---

## PlantUML Diagram

```plantuml
@startuml edX Platform Architecture

skinparam backgroundColor #FFFFFF

cloud "Global Learners\n50M+ Users" as Users

package "Edge Layer" {
    [Route 53] as R53
    [CloudFront CDN] as CF
    [AWS WAF] as WAF
}

package "Application Tier (EKS)" {
    package "Core Services" {
        [LMS] as LMS
        [CMS/Studio] as CMS
        [Ecommerce] as Ecomm
        [Discovery] as Disc
        [Credentials] as Cred
    }
    
    package "Supporting Services" {
        [Notes] as Notes
        [Forums] as Forums
        [Analytics] as Analytics
        [+40 more] as More
    }
}

package "Legacy (ASG)" {
    [EC2 Services] as Legacy
    note right: Migration\nTarget
}

package "Data Layer" {
    database "RDS MySQL\nMulti-AZ" as RDS
    database "ElastiCache\nRedis" as Redis
    database "Elasticsearch\n50+ nodes" as ES
    storage "S3 Storage\nPetabytes" as S3
}

package "GitOps" {
    [ArgoCD] as Argo
    [Helm Charts] as Helm
}

package "Observability" {
    [New Relic] as NR
    [PagerDuty] as PD
    [CloudWatch] as CW
}

Users --> R53
R53 --> CF
CF --> WAF
WAF --> LMS
WAF --> Legacy

LMS --> RDS
LMS --> Redis
LMS --> ES
CMS --> S3

Argo --> LMS
Argo --> CMS
Helm --> Argo

LMS --> NR
NR --> PD
CW --> NR

@enduml
```

---

## On-Call Incident Response Flow

```mermaid
flowchart TB
    subgraph "Alert Trigger"
        MONITOR[Monitoring Alert]
        THRESH[Threshold Breach]
    end

    subgraph "Triage (5 min)"
        PD[PagerDuty Alert]
        ACK[Acknowledge]
        ASSESS[Assess Severity]
    end

    subgraph "Mitigation"
        RUNBOOK[Lookup Runbook]
        FIX[Apply Fix]
        ROLLBACK[Rollback if needed]
    end

    subgraph "Resolution"
        VERIFY[Verify Fixed]
        COMMS[Update Status Page]
        RCA[Root Cause Analysis]
    end

    subgraph "Post-Incident"
        POSTMORTEM[Blameless Postmortem]
        TICKET[Create Follow-up Tickets]
        IMPROVE[Improve Runbooks]
    end

    MONITOR --> THRESH --> PD
    PD --> ACK --> ASSESS
    ASSESS --> RUNBOOK --> FIX
    FIX --> ROLLBACK
    FIX --> VERIFY
    ROLLBACK --> VERIFY
    VERIFY --> COMMS --> RCA
    RCA --> POSTMORTEM --> TICKET --> IMPROVE
```

---

## Service Level Objectives Dashboard

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        edX SLO DASHBOARD                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  SERVICE         │ SLO TARGET │ CURRENT  │ ERROR BUDGET │ STATUS            │
│  ────────────────┼────────────┼──────────┼──────────────┼─────────────────  │
│  LMS Availability│   99.9%    │  99.94%  │  72% remain  │  ✅ Healthy       │
│  API Latency P99 │   <500ms   │   342ms  │     N/A      │  ✅ Healthy       │
│  Video Delivery  │   99.95%   │  99.97%  │  84% remain  │  ✅ Healthy       │
│  Authentication  │   99.99%   │  99.995% │  95% remain  │  ✅ Healthy       │
│  Course Enrollment│  99.9%    │  99.87%  │  43% remain  │  ⚠️ Warning       │
│  ────────────────┴────────────┴──────────┴──────────────┴─────────────────  │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    ERROR BUDGET BURNDOWN (30 days)                      ││
│  │                                                                         ││
│  │  100% │ ─────────────────────────────────────────────────────────────   ││
│  │       │ ╲                                                               ││
│  │   75% │  ╲────────────────────────────────────────────────────────      ││
│  │       │                                         ╲                       ││
│  │   50% │                                          ╲────────────────      ││
│  │       │                                                   ╲             ││
│  │   25% │                                                    ╲────────    ││
│  │       │                                                                 ││
│  │    0% └─────────────────────────────────────────────────────────────    ││
│  │         Day 1                                              Day 30       ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Terraform Module Structure

```mermaid
flowchart TB
    subgraph "Terraform Modules"
        subgraph "Compute"
            EKS[eks-cluster/]
            ASG[auto-scaling/]
        end
        
        subgraph "Database"
            RDS_MOD[rds-mysql/]
            REDIS_MOD[elasticache/]
            ES_MOD[elasticsearch/]
        end
        
        subgraph "Networking"
            VPC[vpc/]
            SG[security-groups/]
            LB[load-balancer/]
        end
        
        subgraph "Storage"
            S3_MOD[s3-buckets/]
            CDN_MOD[cloudfront/]
        end
    end

    subgraph "Environments"
        PROD[production/]
        STG[staging/]
        SAND[sandbox/]
    end

    EKS --> PROD
    EKS --> STG
    EKS --> SAND
    RDS_MOD --> PROD
    RDS_MOD --> STG
    VPC --> PROD
    VPC --> STG
    VPC --> SAND
```

---

## Component Specifications

### EKS Cluster:
| Spec | Value |
|------|-------|
| Node Groups | 3 (general, compute, memory) |
| General Nodes | m5.2xlarge x 20 |
| Compute Nodes | c5.4xlarge x 10 |
| Memory Nodes | r5.2xlarge x 10 |
| Total Pods | 500+ running |

### Database Layer:
| Service | Spec |
|---------|------|
| RDS MySQL | db.r5.4xlarge, Multi-AZ |
| ElastiCache | cache.r5.2xlarge, 6 nodes |
| Elasticsearch | 50+ nodes, i3.2xlarge |

### Microservices:
| Category | Count |
|----------|-------|
| Core Services | 5 |
| Supporting Services | 45+ |
| Background Workers | 20+ |
| Scheduled Jobs | 30+ |
