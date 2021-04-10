# diagram.py
from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.security import Vault
from diagrams.onprem.network import Consul, Ambassador, Kong, Envoy
from diagrams.k8s.network import SVC
from diagrams.gcp.compute import GKE
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.custom import Custom
from diagrams.onprem.iac import Terraform

with Diagram("DevOps Tools Chain", show=False):

    devops_team = Custom("DevOps Team", "./resources/devops.png")

    with Cluster("Documentation"):
        with Cluster("Confluence"):
            documentation = Custom("Confluence (How To's)", "./resources/confluence.png")

        with Cluster("Diagram as Code"):
            diagram_as_code = Custom("Infrastructure Architecture", "./resources/diagram.png")

    with Cluster("Tools Chain"):
        openldap = Custom("OpenLDAP", "./resources/openldap.png")

        with Cluster("CI / CD & Automation"):
            continous_integration = Jenkins("Jenkins Job and Pipeline")
            continous_integration - [Custom("Bitbucket CI", "./resources/bitbucket.png")] << openldap

            devops_team >> continous_integration >> documentation
        
        with Cluster("Provisioning"):
            provisioning = Terraform("Terraform")
            provisioning - [Custom("Packer", "./resources/packer.png"), Custom("Helm", "./resources/helm.png")]

            devops_team >> provisioning >> documentation

        with Cluster("Secret Management"):
            secret_management = Vault("Vault")
            secret_management << Edge(label="collect key/value") << [Consul("Consul")] << openldap

            devops_team >> secret_management >> diagram_as_code

        with Cluster("Edge Stack", direction="LR"):
            edge_stack = Ambassador("Ambassador Ingress Gateway")
            edge_stack >> [Kong("KONG API Gateway")]

            devops_team >> edge_stack >> diagram_as_code

        with Cluster("Service Discovery and Mesh"):
            service_discovery_mesh = Consul("Consul")
            service_discovery_mesh << [Envoy("Consul Connect+Envoy")]

            devops_team >> service_discovery_mesh >> diagram_as_code

        with Cluster("Monitoring and Alerting"):
            monitoring = Prometheus("Prometheus Metric and Alert Manager")
            monitoring >> [Grafana("Dashboard Monitoring")] << openldap

            devops_team >> monitoring >> documentation

        with Cluster("Scheduler and Operational Task"):
            rundeck = Custom("Rundeck", "./resources/rundeck.png")
            rundeck << [openldap]

            devops_team >> rundeck >> documentation
        
        with Cluster("VPN"):
            vpn = Custom("Pritunl", "./resources/pritunl.png")
            vpn << [openldap]

            devops_team >> vpn >> documentation
        
        openldap >> documentation

        with Cluster("Security and Escalation"):
            escalation = Custom("Horangi Warden", "./resources/horangi.png")
            escalation - [Custom("PagerDuty", "./resources/pagerduty.png")]

            devops_team >> escalation >> documentation
    
    with Cluster("Adhoc Request / Supporting"):
        supporting = Custom("JIRA Task", "./resources/jira.png")
        supporting << [Custom("SLA", ""), Custom("Task Resolution", "")]

        devops_team >> supporting >> documentation

    with Cluster("Culture"):
        culture = Custom("Engineering Team", "")
        documentation >> culture
        supporting >> culture

    

        # continous_integration >> documentation
        # provisioning >> documentation
        # secret_management >> documentation
        # edge_stack >> documentation
        # service_discovery_mesh >> documentation
        # openldap >> documentation
        # monitoring >> documentation
        # rundeck >> documentation
        # vpn >> documentation
        # escalation >> documentation
        # supporting >> documentation

        