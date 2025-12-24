# Cisco Live: Global Event Platform (85K+ Peak RPS)

## Project Overview

**Client:** Cisco Systems (via Emumba)  
**Events:** Cisco Live 2020 & 2021  
**Duration:** December 2019 - May 2021  
**Role:** DevOps Architect / Team Lead

---

## Executive Summary

Architected and deployed the infrastructure for Cisco Live's global virtual event platform, scaling to handle 85,000+ requests per second at peak with an average load of 40,000 RPS during the three-day global event. Led a team of 3 engineers, managing infrastructure that scaled to 150 application nodes and 32 database nodes.

---

## Event Scale

| Metric | Value |
|--------|-------|
| Peak RPS | 85,000 |
| Average RPS | 40,000 |
| App Nodes | 150 |
| DB Nodes | 32 |
| Duration | 3 Days |
| Uptime | Zero Downtime |

---

## Infrastructure Architecture

### Architecture Diagrams

![Cisco Live Platform Architecture](diagrams/images/05-cisco-main.png)

![Auto-Scaling Architecture](diagrams/images/05-cisco-scaling.png)

---

## Technical Implementation

### 1. Auto-Scaling Architecture

![Auto-Scaling Architecture](diagrams/images/05-cisco-scaling.png)

**Traffic Pattern:**
- Pre-event baseline → Day 1-3 peak at 85K RPS → Post-event wind-down
- Average sustained load: 40,000 requests/second

**Scaling Rules:**
| Parameter | Value |
|-----------|-------|
| Min Instances | 20 (pre-warmed) |
| Max Instances | 200 |
| Scale-up Trigger | CPU > 60% OR RPS > 500/instance |
| Scale-down Trigger | CPU < 30% for 10 minutes |
| Cooldown Period | 3 minutes |

### 2. Real-Time Monitoring Dashboard

**Key Metrics Monitored (Datadog):**

| Metric | Peak Value | Target |
|--------|------------|--------|
| Request Rate | 85K RPS | Handle 100K+ |
| Error Rate | 0.02% | < 0.1% |
| Latency (p99) | 145ms | < 150ms |
| Instance Count | 150 nodes | Max 200 |
| CPU Utilization | 68% | < 80% |
| Memory Usage | 72% | < 85% |
| DB Connections | 2,400 active | Pool: 15K |
| Cache Hit Rate | 94.7% | > 90% |
| CDN Bandwidth | 12.5 Gbps | - |

### 3. Database Optimization

**Write Path:** Application → Connection Pool (PgBouncer) → Primary Node → Async Replication to 31 Replicas

**Read Path:** Application → Read Replica Load Balancer → 31 Read Replicas (round-robin distribution)

**Optimizations Applied:**
- **Connection Pooling:** PgBouncer with 100 connections per app node
- **Query Optimization:** Indexed hot paths, prepared statements for common queries  
- **Read Replica Routing:** 95% of queries routed to read replicas
- **Replication:** 1 primary + 31 read replicas for horizontal read scaling

### 4. Pre-Event Load Testing

| Phase | Timing | Activities |
|-------|--------|------------|
| **Baseline** | 1 week before | 10K concurrent users, identify bottlenecks, measure baseline metrics |
| **Stress Test** | 3 days before | 100K+ RPS sustained, test auto-scaling triggers, validate failover mechanisms |
| **Chaos Testing** | 2 days before | Simulate node failures, database failover testing, network partition simulation |
| **Dress Rehearsal** | 1 day before | Full event simulation, team readiness check, runbook validation |

---

## Team Leadership

**Team Structure:** DevOps Architect (Team Lead) → 3 DevOps Engineers

**Responsibilities:**
- Architecture decisions and client communication
- Code reviews and mentoring
- Incident escalation point
- Sprint planning and delivery

---

## Key Achievements

| Metric | Result |
|--------|--------|
| Peak Traffic Handled | 85,000 requests/second |
| Average Sustained Load | 40,000 requests/second |
| Application Nodes (Peak) | 150 instances |
| Database Nodes | 32 nodes (1 primary + 31 replicas) |
| Event Duration | 3 days global event |
| Uptime | 100% (zero downtime) |
| P99 Latency | < 150ms |
| Cache Hit Rate | 94.7% |

---

## Technologies Used

**Cloud Platform (GCP):**
- Compute Engine (Managed Instance Groups)
- Cloud Load Balancing
- Cloud CDN
- Cloud SQL / Custom Database Cluster
- Cloud Storage
- Cloud Memorystore (Redis)

**Monitoring & Observability:**
- Datadog (APM, Infrastructure, Logs)
- Custom dashboards and alerts
- Real-time event monitoring

**Infrastructure:**
- Terraform for IaC
- Ansible for configuration management
- Docker for containerization

---

## Lessons Learned

1. **Pre-warming is essential** - Started with 20 nodes instead of minimum to handle initial surge
2. **Cache everything possible** - 94.7% cache hit rate reduced database load dramatically
3. **Read replicas at scale** - 31 read replicas handled 95% of database queries
4. **Real-time monitoring** - Datadog dashboards were critical during the event
5. **Runbook preparation** - Pre-written runbooks for every failure scenario

---

## Contact

**Available for similar projects involving:**
- High-traffic event infrastructure
- Auto-scaling architecture design
- Google Cloud Platform implementation
- Real-time monitoring with Datadog
- Database optimization at scale
- Team leadership for critical projects
