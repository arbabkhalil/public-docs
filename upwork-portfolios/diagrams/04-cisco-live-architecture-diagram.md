# High-Scale Event Platform (Cisco Live) - Architecture Diagram

## Mermaid Diagram - Overall Architecture

```mermaid
flowchart TB
    subgraph "Global Users"
        USERS[👥 Global Attendees<br/>85K peak concurrent]
    end

    subgraph "Edge Layer"
        CDN[Cloud CDN]
        GLB[Global Load Balancer]
        SSL[SSL Termination]
    end

    subgraph "Application Tier"
        subgraph "Auto-Scaling Group"
            N1[Node 01]
            N2[Node 02]
            N3[Node 03]
            NN[Node 150...]
        end
    end

    subgraph "Caching Layer"
        REDIS[Redis Cluster]
        MEMCACHE[Memcached]
    end

    subgraph "Database Tier"
        subgraph "Write Path"
            PRIMARY[(Primary DB)]
        end
        subgraph "Read Path - 31 Replicas"
            R1[(Replica 1)]
            R2[(Replica 2)]
            R3[(Replica 3)]
            RN[(Replica 31...)]
        end
        READLB[Read Load Balancer]
    end

    subgraph "Storage"
        GCS[Cloud Storage]
    end

    subgraph "Monitoring"
        DD[Datadog APM]
    end

    USERS --> CDN --> GLB --> SSL
    SSL --> N1
    SSL --> N2
    SSL --> N3
    SSL --> NN
    
    N1 --> REDIS
    N1 --> MEMCACHE
    N1 --> PRIMARY
    N1 --> READLB
    
    READLB --> R1
    READLB --> R2
    READLB --> R3
    READLB --> RN
    
    PRIMARY --> R1
    PRIMARY --> R2
    PRIMARY --> R3
    PRIMARY --> RN
    
    N1 --> DD
```

---

## Traffic Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant CDN
    participant LB as Load Balancer
    participant App as App Node
    participant Cache as Redis/Memcached
    participant DB as Database

    Note over User,DB: Request Flow (Cache Hit - 95% of requests)
    User->>CDN: Request
    CDN->>LB: Forward (if not cached)
    LB->>App: Route to healthy node
    App->>Cache: Check cache
    Cache-->>App: Cache HIT
    App-->>LB: Response
    LB-->>CDN: Response
    CDN-->>User: Cached Response

    Note over User,DB: Request Flow (Cache Miss - 5% of requests)
    User->>CDN: Request
    CDN->>LB: Forward
    LB->>App: Route
    App->>Cache: Check cache
    Cache-->>App: Cache MISS
    App->>DB: Query (Read Replica)
    DB-->>App: Data
    App->>Cache: Store in cache
    App-->>LB: Response
    LB-->>CDN: Response
    CDN-->>User: Response
```

---

## Auto-Scaling Architecture

```mermaid
flowchart TB
    subgraph "Scaling Trigger"
        METRICS[Metrics Collection]
        CPU[CPU > 60%]
        RPS[RPS > 500/node]
    end

    subgraph "Scaling Decision"
        POLICY[Scaling Policy]
        COOLDOWN[Cooldown: 3min]
    end

    subgraph "Instance Pool"
        subgraph "Minimum (Pre-warmed)"
            MIN1[Node 1-20]
        end
        subgraph "Scaled Instances"
            SCALED[Node 21-150]
        end
        subgraph "Maximum Capacity"
            MAX[Up to 200 nodes]
        end
    end

    METRICS --> CPU
    METRICS --> RPS
    CPU --> POLICY
    RPS --> POLICY
    POLICY --> COOLDOWN
    COOLDOWN --> SCALED

    style MIN1 fill:#90EE90
    style SCALED fill:#FFE4B5
    style MAX fill:#FFB6C1
```

---

## PlantUML Diagram

```plantuml
@startuml Cisco Live Platform Architecture

skinparam backgroundColor #FFFFFF
skinparam componentStyle rectangle

cloud "Global Users\n85K Peak RPS" as Users

package "Edge Layer" {
    [Cloud CDN] as CDN
    [Global Load Balancer] as GLB
    [SSL Termination] as SSL
}

package "Application Tier\n(Auto-Scaling: 20-150 nodes)" {
    [Node 01] as N1
    [Node 02] as N2
    [Node ...] as NN
    [Node 150] as N150
}

package "Caching Layer\n(94.7% Hit Rate)" {
    database "Redis Cluster" as Redis
    database "Memcached" as Memcache
}

package "Database Tier\n(32 Nodes)" {
    database "Primary" as Primary
    
    package "Read Replicas (31)" {
        database "Replica 1" as R1
        database "Replica 2" as R2
        database "..." as RN
        database "Replica 31" as R31
    }
    
    [Read LB] as ReadLB
}

package "Monitoring" {
    [Datadog APM] as DD
    [Alerting] as Alert
}

Users --> CDN
CDN --> GLB
GLB --> SSL
SSL --> N1
SSL --> N2
SSL --> NN
SSL --> N150

N1 --> Redis
N1 --> Memcache
N1 --> Primary : "writes"
N1 --> ReadLB : "reads"

ReadLB --> R1
ReadLB --> R2
ReadLB --> RN
ReadLB --> R31

Primary --> R1 : "replication"
Primary --> R2 : "replication"
Primary --> RN : "replication"
Primary --> R31 : "replication"

N1 --> DD
N2 --> DD
NN --> DD
N150 --> DD
DD --> Alert

@enduml
```

---

## Load Testing Progression

```mermaid
flowchart LR
    subgraph "Phase 1: Baseline"
        P1[10K Users<br/>Identify Bottlenecks]
    end
    
    subgraph "Phase 2: Stress"
        P2[100K+ RPS<br/>Test Auto-scaling]
    end
    
    subgraph "Phase 3: Chaos"
        P3[Failure Simulation<br/>Failover Testing]
    end
    
    subgraph "Phase 4: Dress Rehearsal"
        P4[Full Event Sim<br/>Team Readiness]
    end
    
    P1 --> P2 --> P3 --> P4
    
    style P1 fill:#90EE90
    style P2 fill:#FFE4B5
    style P3 fill:#FFB6C1
    style P4 fill:#ADD8E6
```

---

## Datadog Monitoring Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CISCO LIVE - REAL-TIME DASHBOARD                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐│
│  │   REQUEST RATE       │  │   ERROR RATE         │  │   LATENCY P99        ││
│  │   ━━━━━━━━━━━        │  │   ━━━━━━━━━━━        │  │   ━━━━━━━━━━━        ││
│  │   85,234 req/s       │  │   0.02%              │  │   142ms              ││
│  │   ▲ 12% from avg     │  │   ✓ Below threshold  │  │   ✓ Below 200ms      ││
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘│
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐│
│  │   ACTIVE NODES       │  │   CPU UTILIZATION    │  │   MEMORY USAGE       ││
│  │   ━━━━━━━━━━━        │  │   ━━━━━━━━━━━        │  │   ━━━━━━━━━━━        ││
│  │   147 / 200          │  │   68%                │  │   72%                ││
│  │   Auto-scaling ON    │  │   ▲ Scaling trigger  │  │   ✓ Healthy          ││
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘│
│                                                                              │
│  ┌──────────────────────┐  ┌──────────────────────┐  ┌──────────────────────┐│
│  │   DB CONNECTIONS     │  │   CACHE HIT RATE     │  │   CDN BANDWIDTH      ││
│  │   ━━━━━━━━━━━        │  │   ━━━━━━━━━━━        │  │   ━━━━━━━━━━━        ││
│  │   2,412 active       │  │   94.7%              │  │   12.5 Gbps          ││
│  │   Pool: 80% used     │  │   ▲ Above target     │  │   ✓ Within capacity  ││
│  └──────────────────────┘  └──────────────────────┘  └──────────────────────┘│
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                    TRAFFIC OVER TIME (3-Day Event)                      ││
│  │                                                                         ││
│  │  RPS │                    ┌────┐                                        ││
│  │  80K │                  ┌─┘    └─┐                                      ││
│  │  60K │               ┌──┘        └──┐                                   ││
│  │  40K │    ┌─────────┘              └─────────┐                          ││
│  │  20K │ ───┘                                  └───                       ││
│  │      └───────────────────────────────────────────────────────────────   ││
│  │           Day 1         Day 2         Day 3                             ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### Application Tier:
| Spec | Value |
|------|-------|
| Instance Type | n2-standard-8 (8 vCPU, 32GB) |
| Min Instances | 20 (pre-warmed) |
| Max Instances | 200 |
| Scale-up Trigger | CPU > 60% OR RPS > 500/node |
| Scale-down Trigger | CPU < 30% for 10 min |

### Database Tier:
| Spec | Value |
|------|-------|
| Primary | n2-highmem-32 (32 vCPU, 256GB) |
| Replicas | 31 x n2-highmem-16 |
| Connection Pool | 100 connections/app node |
| Read/Write Split | 95% reads, 5% writes |

### Caching Layer:
| Spec | Value |
|------|-------|
| Redis | 5-node cluster, 64GB each |
| Memcached | 10-node cluster, 32GB each |
| Hit Rate Target | > 90% |
| TTL | 5-15 minutes depending on data |
