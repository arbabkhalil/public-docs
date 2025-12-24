# Architecture Diagrams Generator
# Uses the 'diagrams' library with official cloud provider icons
# Install: pip install diagrams

from diagrams import Diagram, Cluster, Edge
from diagrams.azure.compute import KubernetesServices, ContainerInstances
from diagrams.azure.database import DatabaseForPostgresqlServers, CacheForRedis, CosmosDb
from diagrams.azure.storage import StorageAccounts, BlobStorage
from diagrams.azure.identity import ActiveDirectory
from diagrams.azure.devops import Devops
from diagrams.azure.security import KeyVaults

from diagrams.aws.compute import EKS, EC2, ElasticContainerServiceContainer
from diagrams.aws.database import RDS, ElasticacheForRedis
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront, VPC, VpnGateway, Route53, ElasticLoadBalancing
from diagrams.aws.security import WAF
from diagrams.aws.integration import Eventbridge

from diagrams.gcp.compute import ComputeEngine, GKE
from diagrams.gcp.database import SQL
from diagrams.gcp.network import LoadBalancing, CDN
from diagrams.gcp.operations import Monitoring

from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.storage import PersistentVolume

from diagrams.onprem.gitops import Argocd
from diagrams.onprem.iac import Terraform, Atlantis
from diagrams.onprem.ci import GitlabCI, GithubActions
from diagrams.onprem.vcs import Gitlab, Github
from diagrams.onprem.monitoring import Prometheus, Grafana, Datadog
from diagrams.onprem.security import Vault
from diagrams.onprem.client import User, Users
from diagrams.onprem.container import Docker
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Nginx

from diagrams.generic.device import Mobile, Tablet
from diagrams.generic.storage import Storage
from diagrams.generic.compute import Rack

import os

# Output directory
OUTPUT_DIR = "/Users/arbab.khalil/personal/public-docs/upwork-portfolios/diagrams/images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Graph attributes for better styling
graph_attr = {
    "fontsize": "24",
    "bgcolor": "white",
    "pad": "0.5",
    "splines": "spline",
}

node_attr = {
    "fontsize": "12",
}

edge_attr = {
    "fontsize": "10",
}


def diagram_01_idp_main():
    """Internal Developer Platform - Main Architecture (AERQ)"""
    with Diagram(
        "Internal Developer Platform",
        filename=f"{OUTPUT_DIR}/01-idp-main",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    ):
        # Developer Experience
        with Cluster("Developer Experience"):
            dev = User("Developer")
            gitlab = Gitlab("GitLab Repo")
        
        # CI/CD Pipeline
        with Cluster("CI/CD Pipeline"):
            gitlab_ci = GitlabCI("GitLab CI")
            atlantis = Atlantis("Atlantis IaC")
            argocd = Argocd("ArgoCD")
        
        # Azure Kubernetes Service
        with Cluster("Azure Kubernetes Service"):
            with Cluster("Platform Services"):
                vault = Vault("HashiCorp Vault")
                prometheus = Prometheus("Prometheus")
                ingress = Nginx("Ingress")
            
            with Cluster("Application Namespaces"):
                dev_ns = Pod("Dev")
                stg_ns = Pod("Staging")
                prod_ns = Pod("Production")
        
        # Azure Cloud Services
        with Cluster("Azure Cloud Services"):
            storage = StorageAccounts("Storage")
            postgres = DatabaseForPostgresqlServers("PostgreSQL")
            redis = CacheForRedis("Redis Cache")
            aad = ActiveDirectory("Azure AD")
        
        # Connections
        dev >> gitlab >> gitlab_ci
        gitlab_ci >> atlantis
        gitlab_ci >> argocd
        
        atlantis >> storage
        atlantis >> postgres
        atlantis >> redis
        
        argocd >> dev_ns
        argocd >> stg_ns
        argocd >> prod_ns
        
        aad >> vault
        vault >> [dev_ns, stg_ns, prod_ns]


def diagram_01_idp_gitops():
    """Internal Developer Platform - GitOps Workflow"""
    with Diagram(
        "GitOps Workflow",
        filename=f"{OUTPUT_DIR}/01-idp-gitops",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
    ):
        with Cluster("Source"):
            code = Github("App Code")
            infra = Github("Infra Code")
        
        with Cluster("Build"):
            docker = Docker("Docker Build")
            helm = Docker("Helm Package")
            tf = Terraform("TF Plan")
        
        with Cluster("Deploy"):
            argocd = Argocd("ArgoCD Sync")
            atlantis = Atlantis("Atlantis Apply")
        
        with Cluster("Target"):
            k8s = KubernetesServices("AKS Cluster")
            azure = StorageAccounts("Azure Resources")
        
        code >> docker >> argocd >> k8s
        code >> helm >> argocd
        infra >> tf >> atlantis >> azure


def diagram_02_edge_cloud_main():
    """Hybrid Edge-Cloud Architecture - Main (ChaiOne TMS)"""
    with Diagram(
        "Hybrid Edge-Cloud Architecture",
        filename=f"{OUTPUT_DIR}/02-edge-cloud-main",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
    ):
        # AWS Cloud
        with Cluster("AWS Cloud Region"):
            with Cluster("Control Plane - EKS"):
                api = EKS("TMS API")
                registry = EKS("Device Registry")
            
            with Cluster("AWS Services"):
                cdn = CloudFront("CloudFront")
                s3 = S3("S3 Storage")
                rds = RDS("PostgreSQL")
            
            vpn = VpnGateway("VPN Gateway")
        
        # Edge Locations
        with Cluster("Edge Location A"):
            edge_a = EC2("Edge Device\nCoreOS + K3s")
            term_a = Mobile("Terminals")
        
        with Cluster("Edge Location B"):
            edge_b = EC2("Edge Device\nCoreOS + K3s")
            term_b = Mobile("Terminals")
        
        with Cluster("Edge Location N"):
            edge_n = EC2("Edge Device\nCoreOS + K3s")
            term_n = Mobile("Terminals")
        
        # Connections
        api >> rds
        api >> s3
        cdn >> s3
        
        vpn >> Edge(label="VPN", style="dashed") >> edge_a
        vpn >> Edge(label="VPN", style="dashed") >> edge_b
        vpn >> Edge(label="VPN", style="dashed") >> edge_n
        
        edge_a >> term_a
        edge_b >> term_b
        edge_n >> term_n
        
        edge_a >> Edge(label="Sync", style="dotted") >> api
        edge_b >> Edge(label="Sync", style="dotted") >> api
        edge_n >> Edge(label="Sync", style="dotted") >> api


def diagram_03_hcl_main():
    """HCL Commerce Kubernetes Migration - Main Architecture"""
    with Diagram(
        "HCL Commerce on AKS",
        filename=f"{OUTPUT_DIR}/03-hcl-main",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
    ):
        # CI/CD
        with Cluster("CI/CD"):
            ado = Devops("Azure DevOps")
            helm = Docker("Helm Charts")
        
        # Azure Cloud
        with Cluster("Azure Cloud"):
            with Cluster("Azure Kubernetes Service"):
                with Cluster("HCL Commerce v9"):
                    store = Pod("Store Server")
                    search = Pod("Search Server")
                    auth = Pod("Auth Server")
                    ts = Pod("Transaction")
                
                with Cluster("Platform Services"):
                    argocd = Argocd("ArgoCD")
                    vault = KeyVaults("SOPS/Vault")
                    ingress = Nginx("Ingress")
            
            with Cluster("Azure Managed Services"):
                sql = DatabaseForPostgresqlServers("Azure SQL")
                blob = BlobStorage("Blob Storage")
                redis = CacheForRedis("Redis Cache")
        
        # Connections
        ado >> argocd
        helm >> argocd
        vault >> argocd
        
        argocd >> store
        argocd >> search
        argocd >> auth
        argocd >> ts
        
        store >> sql
        store >> blob
        store >> redis


def diagram_03_hcl_bluegreen():
    """HCL Commerce - Blue-Green Deployment"""
    with Diagram(
        "Blue-Green Deployment",
        filename=f"{OUTPUT_DIR}/03-hcl-bluegreen",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
    ):
        with Cluster("Before"):
            b_svc = Service("Active Service")
            b_blue = Deployment("v1.0.0 (Blue)")
            b_svc >> b_blue
        
        with Cluster("During Deployment"):
            d_asvc = Service("Active Svc")
            d_psvc = Service("Preview Svc")
            d_blue = Deployment("v1.0.0")
            d_green = Deployment("v1.1.0")
            d_asvc >> d_blue
            d_psvc >> d_green
        
        with Cluster("After Promotion"):
            a_svc = Service("Active Service")
            a_green = Deployment("v1.1.0 (Green)")
            a_svc >> a_green


def diagram_04_edx_main():
    """edX Platform - SRE Architecture"""
    with Diagram(
        "edX Platform Architecture",
        filename=f"{OUTPUT_DIR}/04-edx-main",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
    ):
        # Users
        users = Users("50M+ Learners")
        
        # Edge
        with Cluster("Edge & CDN"):
            r53 = Route53("Route 53")
            cf = CloudFront("CloudFront")
            waf = WAF("AWS WAF")
        
        # EKS
        with Cluster("EKS Cluster"):
            with Cluster("Core Services"):
                lms = EKS("LMS")
                cms = EKS("CMS/Studio")
                ecomm = EKS("Ecommerce")
            
            with Cluster("Supporting"):
                notes = Pod("Notes")
                forums = Pod("Forums")
                more = Pod("+40 more")
        
        # Legacy
        with Cluster("Legacy ASG"):
            ec2 = EC2("EC2 Services")
        
        # Data
        with Cluster("Data Layer"):
            rds = RDS("RDS MySQL")
            redis = ElasticacheForRedis("ElastiCache")
            s3 = S3("S3 Storage")
        
        # GitOps
        with Cluster("GitOps"):
            argocd = Argocd("ArgoCD")
        
        # Observability
        with Cluster("Observability"):
            datadog = Datadog("Datadog/NewRelic")
        
        # Connections
        users >> r53 >> cf >> waf
        waf >> lms
        waf >> ec2
        
        lms >> rds
        lms >> redis
        cms >> s3
        
        argocd >> lms
        argocd >> cms
        
        lms >> datadog


def diagram_04_edx_migration():
    """edX - Migration Flow"""
    with Diagram(
        "EC2 to EKS Migration",
        filename=f"{OUTPUT_DIR}/04-edx-migration",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
    ):
        with Cluster("Source: EC2"):
            ec2 = EC2("EC2 Instances")
        
        with Cluster("Migration Process"):
            docker = Docker("1. Containerize")
            helm = Docker("2. Helm Chart")
            test = EKS("3. Parallel Test")
        
        with Cluster("Target: EKS"):
            eks = EKS("EKS Cluster")
            argocd = Argocd("ArgoCD")
        
        ec2 >> docker >> helm >> test >> eks
        argocd >> eks


def diagram_05_cisco_main():
    """Cisco Live - High-Scale Event Platform"""
    with Diagram(
        "Cisco Live Platform - 85K RPS",
        filename=f"{OUTPUT_DIR}/05-cisco-main",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
    ):
        # Users
        users = Users("85K Peak RPS")
        
        # Edge
        with Cluster("Edge Layer"):
            cdn = CDN("Cloud CDN")
            lb = LoadBalancing("Global LB")
        
        # App Tier
        with Cluster("Application Tier - Auto Scaling"):
            with Cluster("150 Nodes"):
                n1 = ComputeEngine("Node 01")
                n2 = ComputeEngine("Node 02")
                n3 = ComputeEngine("Node ...")
                n150 = ComputeEngine("Node 150")
        
        # Cache
        with Cluster("Caching Layer"):
            redis = Redis("Redis Cluster")
        
        # Database
        with Cluster("Database Tier"):
            with Cluster("Write Path"):
                primary = SQL("Primary DB")
            with Cluster("Read Path - 31 Replicas"):
                r1 = SQL("Replica 1")
                r2 = SQL("Replica 2")
                rn = SQL("Replica 31")
        
        # Monitoring
        datadog = Datadog("Datadog APM")
        
        # Connections
        users >> cdn >> lb
        lb >> n1
        lb >> n2
        lb >> n3
        lb >> n150
        
        n1 >> redis
        n1 >> primary
        n1 >> r1
        
        primary >> Edge(style="dashed") >> r1
        primary >> Edge(style="dashed") >> r2
        primary >> Edge(style="dashed") >> rn
        
        n1 >> datadog


def diagram_05_cisco_scaling():
    """Cisco Live - Auto-Scaling Architecture"""
    with Diagram(
        "Auto-Scaling Architecture",
        filename=f"{OUTPUT_DIR}/05-cisco-scaling",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
    ):
        with Cluster("Metrics"):
            monitoring = Monitoring("CPU/RPS Metrics")
        
        with Cluster("Scaling Decision"):
            policy = Monitoring("Scaling Policy")
        
        with Cluster("Instance Pool"):
            min_nodes = ComputeEngine("Min: 20\nPre-warmed")
            scaled = ComputeEngine("Scaled: 21-150")
            max_nodes = ComputeEngine("Max: 200")
        
        monitoring >> policy
        policy >> scaled
        min_nodes >> scaled >> max_nodes


def diagram_02_edge_device():
    """Edge Device Architecture - K3s on CoreOS"""
    with Diagram(
        "Edge Device Architecture",
        filename=f"{OUTPUT_DIR}/02-edge-device",
        show=False,
        direction="TB",
        graph_attr=graph_attr,
    ):
        with Cluster("Edge Device (CoreOS)"):
            with Cluster("K3s Cluster"):
                agent = Pod("TMS Agent")
                sync = Pod("Sync Service")
                localdb = PostgreSQL("Local DB")
                config = Pod("Config Watcher")
            
            with Cluster("System Services"):
                vpn_client = Nginx("VPN Client")
                updates = Docker("Auto Updates")
                monitor = Prometheus("Monitoring")
        
        cloud = EKS("Cloud API")
        terminals = Mobile("Terminals")
        
        agent >> localdb
        sync >> cloud
        agent >> terminals
        vpn_client >> cloud


def diagram_02_cicd_pipeline():
    """Edge-Cloud CI/CD Pipeline"""
    with Diagram(
        "CI/CD Pipeline",
        filename=f"{OUTPUT_DIR}/02-cicd-pipeline",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
    ):
        with Cluster("Source"):
            commit = Github("Commit Code")
        
        with Cluster("Build"):
            build = Docker("Build Docker")
            test = Docker("Run E2E Tests")
        
        with Cluster("Cloud Deploy"):
            staging = EKS("Staging EKS")
            prod = EKS("Production EKS")
        
        with Cluster("Edge Deploy"):
            iso = Docker("Edge ISO Build")
            edge = EC2("Edge Devices")
        
        commit >> build >> test >> staging >> prod
        test >> iso >> edge


def diagram_04_incident_response():
    """edX - Incident Response Flow"""
    with Diagram(
        "Incident Response Flow",
        filename=f"{OUTPUT_DIR}/04-incident-response",
        show=False,
        direction="LR",
        graph_attr=graph_attr,
    ):
        with Cluster("Detection"):
            alert = Datadog("Alert Trigger")
        
        with Cluster("Response"):
            page = User("PagerDuty")
            triage = User("Triage (5min)")
        
        with Cluster("Resolution"):
            runbook = Docker("Runbook Lookup")
            fix = EKS("Rollback/Fix")
        
        with Cluster("Post-Incident"):
            rca = Docker("RCA & Postmortem")
        
        alert >> page >> triage >> runbook >> fix >> rca


if __name__ == "__main__":
    print("Generating architecture diagrams...")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Generate all diagrams
    print("\n1. Internal Developer Platform (AERQ)...")
    diagram_01_idp_main()
    diagram_01_idp_gitops()
    
    print("2. Hybrid Edge-Cloud Architecture (ChaiOne)...")
    diagram_02_edge_cloud_main()
    diagram_02_edge_device()
    diagram_02_cicd_pipeline()
    
    print("3. HCL Commerce Migration (Parker)...")
    diagram_03_hcl_main()
    diagram_03_hcl_bluegreen()
    
    print("4. edX SRE Platform...")
    diagram_04_edx_main()
    diagram_04_edx_migration()
    diagram_04_incident_response()
    
    print("5. Cisco Live Event Platform...")
    diagram_05_cisco_main()
    diagram_05_cisco_scaling()
    
    print("\n✅ All diagrams generated successfully!")
    print(f"📁 Check: {OUTPUT_DIR}")
