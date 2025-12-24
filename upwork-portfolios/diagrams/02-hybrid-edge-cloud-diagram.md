# Hybrid Edge-Cloud Architecture - Diagram

## Mermaid Diagram

```mermaid
flowchart TB
    subgraph "AWS Cloud Region"
        subgraph "Control Plane - EKS"
            API[TMS API Gateway]
            ANALYTICS[Analytics Service]
            REGISTRY[Device Registry]
            CONFIG[Config Manager]
        end
        
        subgraph "AWS Services"
            CF[CloudFront CDN]
            S3[S3 Storage]
            RDS[(RDS PostgreSQL)]
            ECR[ECR Registry]
        end
        
        VPN[AWS VPN Gateway]
    end

    subgraph "Edge Location A"
        subgraph "Edge Device A - CoreOS"
            K3S_A[K3s Cluster]
            AGENT_A[TMS Agent]
            LOCALDB_A[(Local SQLite)]
        end
        TERMINALS_A[🖥️ Terminals]
    end

    subgraph "Edge Location B"
        subgraph "Edge Device B - CoreOS"
            K3S_B[K3s Cluster]
            AGENT_B[TMS Agent]
            LOCALDB_B[(Local SQLite)]
        end
        TERMINALS_B[🖥️ Terminals]
    end

    subgraph "Edge Location N"
        subgraph "Edge Device N - CoreOS"
            K3S_N[K3s Cluster]
            AGENT_N[TMS Agent]
            LOCALDB_N[(Local SQLite)]
        end
        TERMINALS_N[🖥️ Terminals]
    end

    API --> RDS
    API --> S3
    CF --> S3
    
    VPN -.->|Site-to-Site VPN| K3S_A
    VPN -.->|Site-to-Site VPN| K3S_B
    VPN -.->|Site-to-Site VPN| K3S_N
    
    AGENT_A --> LOCALDB_A
    AGENT_B --> LOCALDB_B
    AGENT_N --> LOCALDB_N
    
    K3S_A --> TERMINALS_A
    K3S_B --> TERMINALS_B
    K3S_N --> TERMINALS_N
    
    AGENT_A -.->|Sync when connected| API
    AGENT_B -.->|Sync when connected| API
    AGENT_N -.->|Sync when connected| API
```

---

## PlantUML Diagram

```plantuml
@startuml Hybrid Edge-Cloud TMS Architecture

skinparam backgroundColor #FFFFFF
skinparam componentStyle rectangle

cloud "AWS Cloud Region" {
    package "Control Plane (EKS)" {
        [TMS API Gateway] as API
        [Analytics Service] as Analytics
        [Device Registry] as Registry
        [Config Manager] as Config
    }
    
    package "AWS Services" {
        [CloudFront CDN] as CF
        [S3 Storage] as S3
        database "RDS PostgreSQL" as RDS
        [ECR Registry] as ECR
    }
    
    [VPN Gateway] as VPN
}

package "Edge Location A" {
    package "Edge Device (CoreOS)" as EdgeA {
        [K3s Cluster] as K3sA
        [TMS Agent] as AgentA
        database "Local SQLite" as LocalA
    }
    [Terminals] as TermA
}

package "Edge Location B" {
    package "Edge Device (CoreOS)" as EdgeB {
        [K3s Cluster] as K3sB
        [TMS Agent] as AgentB
        database "Local SQLite" as LocalB
    }
    [Terminals] as TermB
}

package "Edge Location N" {
    package "Edge Device (CoreOS)" as EdgeN {
        [K3s Cluster] as K3sN
        [TMS Agent] as AgentN
        database "Local SQLite" as LocalN
    }
    [Terminals] as TermN
}

API --> RDS
CF --> S3

VPN ..> K3sA : "Site-to-Site VPN"
VPN ..> K3sB : "Site-to-Site VPN"
VPN ..> K3sN : "Site-to-Site VPN"

AgentA --> LocalA
AgentB --> LocalB
AgentN --> LocalN

K3sA --> TermA
K3sB --> TermB
K3sN --> TermN

AgentA ..> API : "Sync"
AgentB ..> API : "Sync"
AgentN ..> API : "Sync"

@enduml
```

---

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant Terminal
    participant EdgeAgent as Edge TMS Agent
    participant LocalDB as Local Database
    participant VPN as VPN Tunnel
    participant CloudAPI as Cloud API
    participant CloudDB as Cloud Database

    Note over Terminal,CloudDB: Normal Operation (Connected)
    Terminal->>EdgeAgent: Transaction Request
    EdgeAgent->>LocalDB: Store Locally
    EdgeAgent->>VPN: Sync Request
    VPN->>CloudAPI: Forward Request
    CloudAPI->>CloudDB: Persist Data
    CloudAPI-->>VPN: Acknowledgment
    VPN-->>EdgeAgent: Sync Complete
    EdgeAgent-->>Terminal: Confirmation

    Note over Terminal,CloudDB: Offline Operation
    Terminal->>EdgeAgent: Transaction Request
    EdgeAgent->>LocalDB: Store Locally
    EdgeAgent-->>Terminal: Confirmation (Queued)
    
    Note over Terminal,CloudDB: Reconnection & Sync
    VPN->>EdgeAgent: Connection Restored
    EdgeAgent->>LocalDB: Get Queued Items
    EdgeAgent->>VPN: Batch Sync
    VPN->>CloudAPI: Forward Batch
    CloudAPI->>CloudDB: Persist All
    CloudAPI-->>EdgeAgent: Sync Complete
```

---

## Component Details for Design Tools

### Cloud Layer Components:
| Component | Icon | Description |
|-----------|------|-------------|
| EKS Cluster | AWS EKS icon | Kubernetes control plane |
| RDS PostgreSQL | Database icon | Central database |
| S3 | Storage bucket icon | Asset storage |
| CloudFront | CDN icon | Content delivery |
| VPN Gateway | Network icon | Secure tunnel endpoint |
| ECR | Container icon | Docker registry |

### Edge Layer Components:
| Component | Icon | Description |
|-----------|------|-------------|
| CoreOS | Server icon | Immutable Linux OS |
| K3s | Kubernetes icon (small) | Lightweight K8s |
| TMS Agent | Application icon | Main edge application |
| SQLite | Database icon (small) | Local persistence |
| Terminals | Monitor icons | End-user devices |

### Connection Types:
| Connection | Style | Description |
|------------|-------|-------------|
| VPN Tunnel | Dashed line | Encrypted tunnel |
| Data Flow | Solid arrow | Direct communication |
| Sync | Dotted arrow | Periodic synchronization |
