"""Script to populate initial knowledge base with technology stacks."""

import logging
from models import TechnologyCategory
from knowledge_base import get_kb_manager
from database import init_database
from config import load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def populate_knowledge_base():
    """Populate knowledge base with initial technology documentation."""
    
    # Initialize
    load_settings()
    init_database()
    kb_manager = get_kb_manager()
    
    logger.info("Populating knowledge base...")
    
    knowledge_entries = [
        # Orchestration
        {
            "technology_name": "Ansible",
            "category": TechnologyCategory.ORCHESTRATION,
            "content": """**Ansible** is an open-source automation tool for configuration management, application deployment, and task automation.

**Key Concepts:**
- Playbooks: YAML files defining automation tasks
- Inventory: List of managed hosts
- Roles: Reusable automation components
- Modules: Units of code Ansible executes

**Common Commands:**
- `ansible-playbook playbook.yml` - Run a playbook
- `ansible all -m ping` - Test connectivity to all hosts
- `ansible-playbook playbook.yml --check` - Dry run mode

**Best Practices:**
- Use roles for organization
- Keep playbooks idempotent
- Use variables for flexibility
- Version control your playbooks
- Use vault for sensitive data

**Troubleshooting:**
- Check SSH connectivity first
- Use -vvv for verbose output
- Verify inventory file syntax
- Check Python version on managed nodes""",
            "keywords": ["ansible", "playbook", "automation", "configuration management", "devops"],
            "created_by": "system"
        },
        {
            "technology_name": "Kubernetes",
            "category": TechnologyCategory.ORCHESTRATION,
            "content": """**Kubernetes (K8s)** is an open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

**Core Components:**
- Pods: Smallest deployable units
- Deployments: Manage replicated applications
- Services: Expose applications
- ConfigMaps/Secrets: Configuration management
- Namespaces: Resource isolation

**Common Commands:**
- `kubectl get pods` - List pods
- `kubectl apply -f deployment.yaml` - Apply configuration
- `kubectl logs <pod-name>` - View logs
- `kubectl describe pod <pod-name>` - Get pod details
- `kubectl exec -it <pod-name> -- /bin/bash` - Shell into pod

**Best Practices:**
- Use namespaces for isolation
- Set resource limits and requests
- Use liveness and readiness probes
- Implement proper RBAC
- Use helm for package management

**Troubleshooting:**
- Check pod status and events
- Review container logs
- Verify resource availability
- Check network policies""",
            "keywords": ["kubernetes", "k8s", "containers", "orchestration", "pods", "kubectl"],
            "created_by": "system"
        },
        {
            "technology_name": "OpenShift",
            "category": TechnologyCategory.ORCHESTRATION,
            "content": """**OpenShift** is Red Hat's enterprise Kubernetes platform with additional developer and operational features.

**Key Features:**
- Built on Kubernetes
- Integrated CI/CD with Jenkins
- Source-to-Image (S2I) builds
- Routes for external access
- Enhanced security with SCC

**Common Commands:**
- `oc login` - Login to cluster
- `oc new-app` - Create new application
- `oc get routes` - List routes
- `oc logs <pod-name>` - View logs
- `oc project <project-name>` - Switch project

**Best Practices:**
- Use projects for multi-tenancy
- Leverage S2I for builds
- Use routes for ingress
- Implement proper RBAC
- Use persistent volumes for stateful apps

**Troubleshooting:**
- Check build logs
- Verify route configuration
- Review security context constraints
- Check project quotas""",
            "keywords": ["openshift", "oc", "kubernetes", "redhat", "containers"],
            "created_by": "system"
        },
        {
            "technology_name": "Puppet",
            "category": TechnologyCategory.ORCHESTRATION,
            "content": """**Puppet** is a configuration management tool for automating infrastructure provisioning and management.

**Core Concepts:**
- Manifests: Puppet code files (.pp)
- Modules: Reusable code collections
- Hiera: Hierarchical data lookup
- Facts: System information
- Catalog: Compiled configuration

**Common Commands:**
- `puppet apply manifest.pp` - Apply manifest
- `puppet agent -t` - Run agent manually
- `puppet module install <module>` - Install module
- `facter` - Display system facts

**Best Practices:**
- Use modules from Puppet Forge
- Organize code with roles and profiles
- Use Hiera for data separation
- Version control your code
- Test with rspec-puppet

**Troubleshooting:**
- Check puppet agent logs
- Verify catalog compilation
- Review master/agent connectivity
- Check certificate issues""",
            "keywords": ["puppet", "configuration management", "automation", "manifest", "hiera"],
            "created_by": "system"
        },
        
        # Containerization
        {
            "technology_name": "Docker",
            "category": TechnologyCategory.CONTAINERIZATION,
            "content": """**Docker** is a platform for developing, shipping, and running applications in containers.

**Key Concepts:**
- Images: Read-only templates
- Containers: Running instances of images
- Dockerfile: Image build instructions
- Registry: Image repository (Docker Hub)
- Volumes: Persistent data storage

**Common Commands:**
- `docker build -t name:tag .` - Build image
- `docker run -d -p 8080:80 image` - Run container
- `docker ps` - List running containers
- `docker logs <container-id>` - View logs
- `docker exec -it <container-id> /bin/bash` - Shell into container
- `docker-compose up -d` - Start services with compose

**Best Practices:**
- Use official base images
- Minimize layers in Dockerfile
- Use .dockerignore
- Don't run as root
- Use multi-stage builds
- Tag images properly

**Troubleshooting:**
- Check container logs
- Verify port mappings
- Review resource constraints
- Check network connectivity
- Inspect container with `docker inspect`""",
            "keywords": ["docker", "containers", "dockerfile", "images", "containerization"],
            "created_by": "system"
        },
        
        # Infrastructure as Code
        {
            "technology_name": "Terraform",
            "category": TechnologyCategory.INFRASTRUCTURE_AS_CODE,
            "content": """**Terraform** is an infrastructure as code tool for building, changing, and versioning infrastructure safely and efficiently.

**Core Concepts:**
- Providers: Cloud/service integrations
- Resources: Infrastructure components
- State: Current infrastructure state
- Modules: Reusable configurations
- Variables: Parameterized configs

**Common Commands:**
- `terraform init` - Initialize working directory
- `terraform plan` - Preview changes
- `terraform apply` - Apply changes
- `terraform destroy` - Destroy infrastructure
- `terraform fmt` - Format code
- `terraform validate` - Validate configuration

**Best Practices:**
- Use remote state (S3, Terraform Cloud)
- Version control your code
- Use modules for reusability
- Implement proper naming conventions
- Use workspaces for environments
- Run plan before apply

**Troubleshooting:**
- Check provider credentials
- Verify state lock status
- Review dependency graph
- Use terraform show for state inspection
- Check for API rate limits""",
            "keywords": ["terraform", "infrastructure as code", "iac", "provisioning", "cloud"],
            "created_by": "system"
        },
        
        # CI/CD
        {
            "technology_name": "GitLab CI",
            "category": TechnologyCategory.CI_CD,
            "content": """**GitLab CI/CD** is a continuous integration and deployment tool integrated into GitLab.

**Key Concepts:**
- .gitlab-ci.yml: Pipeline configuration
- Stages: Sequential phases
- Jobs: Tasks within stages
- Runners: Execution agents
- Artifacts: Build outputs
- Variables: Configuration parameters

**Pipeline Stages:**
- Build: Compile code
- Test: Run tests
- Deploy: Deploy to environments

**Common Patterns:**
```yaml
stages:
  - build
  - test
  - deploy

build_job:
  stage: build
  script:
    - make build
```

**Best Practices:**
- Use caching for dependencies
- Parallelize jobs when possible
- Use CI/CD variables for secrets
- Implement proper error handling
- Use artifacts for inter-job data
- Tag runners appropriately

**Troubleshooting:**
- Check runner availability
- Review job logs
- Verify .gitlab-ci.yml syntax
- Check variables and secrets
- Verify Docker image availability""",
            "keywords": ["gitlab", "ci/cd", "pipeline", "automation", "devops"],
            "created_by": "system"
        },
        {
            "technology_name": "Argo CD",
            "category": TechnologyCategory.CI_CD,
            "content": """**Argo CD** is a declarative GitOps continuous delivery tool for Kubernetes.

**Key Concepts:**
- Applications: Deployed K8s resources
- Projects: Logical grouping
- Repositories: Git repos with manifests
- Sync: Deploy from Git to cluster
- Health Status: Application state

**Common Operations:**
- Create application from Git repo
- Sync application with cluster
- Rollback to previous version
- Auto-sync for GitOps
- Multi-cluster deployment

**Best Practices:**
- Use App of Apps pattern
- Implement proper RBAC
- Use sync waves for ordering
- Leverage hooks for migrations
- Monitor sync status
- Use automated sync policies

**Troubleshooting:**
- Check application sync status
- Review sync errors
- Verify Git repository access
- Check cluster connectivity
- Review resource hooks""",
            "keywords": ["argocd", "gitops", "kubernetes", "ci/cd", "deployment"],
            "created_by": "system"
        },
        
        # Monitoring & Logging
        {
            "technology_name": "ELK Stack",
            "category": TechnologyCategory.MONITORING_LOGGING,
            "content": """**ELK Stack** (Elasticsearch, Logstash, Kibana) is a log management and analytics platform.

**Components:**
- Elasticsearch: Search and analytics engine
- Logstash: Data processing pipeline
- Kibana: Visualization platform
- Beats: Lightweight data shippers

**Common Use Cases:**
- Centralized logging
- Log analysis
- Real-time monitoring
- Security analytics
- Metrics visualization

**Best Practices:**
- Use index patterns
- Implement retention policies
- Set up proper sharding
- Use filebeat for log shipping
- Create meaningful visualizations
- Implement security (X-Pack)
- Monitor cluster health

**Troubleshooting:**
- Check Elasticsearch cluster health
- Verify index mappings
- Review Logstash pipeline
- Check disk space
- Monitor JVM heap usage""",
            "keywords": ["elk", "elasticsearch", "logstash", "kibana", "logging", "monitoring"],
            "created_by": "system"
        },
        {
            "technology_name": "Prometheus & Grafana",
            "category": TechnologyCategory.MONITORING_LOGGING,
            "content": """**Prometheus** is a monitoring system with time series database. **Grafana** is a visualization platform.

**Prometheus Concepts:**
- Metrics: Time series data
- Targets: Monitored endpoints
- PromQL: Query language
- Alertmanager: Alert handling
- Exporters: Metric collectors

**Grafana Features:**
- Dashboards: Visual displays
- Data sources: Multiple backends
- Alerts: Notification rules
- Plugins: Extended functionality

**Common Queries (PromQL):**
```
rate(http_requests_total[5m])
up{job="api-server"}
```

**Best Practices:**
- Use service discovery
- Set up proper labels
- Create meaningful dashboards
- Configure alert rules
- Use recording rules for complex queries
- Implement retention policies

**Troubleshooting:**
- Check target status
- Verify scrape intervals
- Review metric cardinality
- Check Grafana datasource
- Validate PromQL queries""",
            "keywords": ["prometheus", "grafana", "monitoring", "metrics", "alerting", "dashboard"],
            "created_by": "system"
        },
        {
            "technology_name": "Zabbix",
            "category": TechnologyCategory.MONITORING_LOGGING,
            "content": """**Zabbix** is an enterprise-class open source monitoring solution.

**Key Components:**
- Server: Central component
- Agent: Data collector on hosts
- Frontend: Web interface
- Database: Data storage
- Proxy: Distributed monitoring

**Monitoring Items:**
- Host availability
- CPU, memory, disk metrics
- Network performance
- Application metrics
- Custom scripts

**Common Tasks:**
- Add hosts to monitoring
- Create templates
- Configure triggers
- Set up actions and notifications
- Create custom items
- Design dashboards

**Best Practices:**
- Use templates for scalability
- Implement proper triggers
- Set up maintenance windows
- Use macros for flexibility
- Regular database maintenance
- Monitor Zabbix server itself

**Troubleshooting:**
- Check agent connectivity
- Verify item keys
- Review trigger expressions
- Check database performance
- Validate network connectivity""",
            "keywords": ["zabbix", "monitoring", "agent", "metrics", "alerts"],
            "created_by": "system"
        },
        
        # Databases
        {
            "technology_name": "MySQL",
            "category": TechnologyCategory.DATABASE,
            "content": """**MySQL** is an open-source relational database management system.

**Key Features:**
- ACID compliance
- Replication support
- InnoDB storage engine
- Full-text search
- Stored procedures
- Triggers and views

**Common Commands:**
```sql
SHOW DATABASES;
USE database_name;
SHOW TABLES;
DESCRIBE table_name;
SELECT * FROM table WHERE condition;
```

**Administration:**
- `mysqldump` for backups
- `mysql` client for queries
- Performance tuning with my.cnf
- Replication setup (master-slave)
- User management

**Best Practices:**
- Regular backups
- Use InnoDB for transactions
- Implement proper indexing
- Monitor slow query log
- Set up replication for HA
- Use connection pooling
- Secure with proper user permissions

**Troubleshooting:**
- Check error logs
- Review slow query log
- Verify connection limits
- Check disk space
- Monitor replication lag""",
            "keywords": ["mysql", "database", "sql", "mariadb", "rdbms"],
            "created_by": "system"
        },
        {
            "technology_name": "PostgreSQL",
            "category": TechnologyCategory.DATABASE,
            "content": """**PostgreSQL** is a powerful open-source object-relational database system.

**Key Features:**
- ACID compliance
- Advanced data types (JSON, arrays)
- Full ACID transactions
- Extensibility
- MVCC for concurrency
- Robust replication

**Common Commands:**
```sql
\\l - List databases
\\c database_name - Connect to database
\\dt - List tables
\\d table_name - Describe table
SELECT * FROM table WHERE condition;
```

**Administration:**
- `pg_dump` for backups
- `psql` client for queries
- `postgresql.conf` for configuration
- Streaming replication
- Vacuum and analyze

**Best Practices:**
- Regular VACUUM operations
- Use appropriate indexes
- Monitor query performance
- Set up streaming replication
- Configure connection pooling (pgBouncer)
- Use EXPLAIN for query optimization
- Implement proper backup strategy

**Troubleshooting:**
- Check PostgreSQL logs
- Review pg_stat_activity
- Monitor connection count
- Check disk I/O
- Analyze slow queries with pg_stat_statements""",
            "keywords": ["postgresql", "postgres", "database", "sql", "psql"],
            "created_by": "system"
        },
        
        # Networking
        {
            "technology_name": "Cisco Networking",
            "category": TechnologyCategory.NETWORKING,
            "content": """**Cisco** networking devices and technologies for enterprise networking.

**Common Devices:**
- Routers: Network routing
- Switches: Layer 2/3 switching
- Firewalls: Security appliances
- Wireless: Access points

**Common Commands (IOS):**
```
show running-config
show ip interface brief
show vlan brief
configure terminal
write memory
```

**Key Concepts:**
- VLANs: Virtual LANs
- Routing protocols (OSPF, EIGRP, BGP)
- Access Control Lists (ACLs)
- Spanning Tree Protocol (STP)
- Port security

**Best Practices:**
- Document network topology
- Use consistent naming conventions
- Implement proper VLANs
- Configure port security
- Regular backups of configs
- Monitor with SNMP
- Use SSH instead of Telnet

**Troubleshooting:**
- Check interface status
- Verify routing tables
- Review ACL configurations
- Test connectivity with ping
- Check VLAN assignments
- Review logs""",
            "keywords": ["cisco", "networking", "router", "switch", "vlan", "ios"],
            "created_by": "system"
        },
        {
            "technology_name": "MikroTik",
            "category": TechnologyCategory.NETWORKING,
            "content": """**MikroTik** RouterOS is a powerful router and firewall operating system.

**Key Features:**
- Routing (OSPF, BGP, RIP)
- Firewall and NAT
- VPN (PPTP, L2TP, IPSec, OpenVPN)
- Wireless access points
- Bandwidth management (Queues)
- Hotspot gateway

**Common Tools:**
- WinBox: GUI management
- WebFig: Web interface
- Terminal: CLI access

**Configuration Tasks:**
- IP addressing
- DHCP server setup
- Firewall rules
- NAT configuration
- VPN setup
- Wireless configuration
- Queue management

**Best Practices:**
- Regular backups
- Use secure password
- Disable unused services
- Implement firewall rules
- Monitor with SNMP
- Keep RouterOS updated
- Document configurations

**Troubleshooting:**
- Check log messages
- Use torch for traffic monitoring
- Review firewall rules
- Test with ping and traceroute
- Check interface status
- Review routing table""",
            "keywords": ["mikrotik", "routeros", "networking", "router", "winbox"],
            "created_by": "system"
        },
        
        # Operating Systems
        {
            "technology_name": "Linux Administration",
            "category": TechnologyCategory.OPERATING_SYSTEM,
            "content": """**Linux Administration** covers system management tasks for Linux servers.

**Core Areas:**
- User and group management
- File system management
- Package management (apt, yum, dnf)
- Service management (systemd)
- Network configuration
- Security (firewall, SELinux)
- Monitoring and logging

**Common Commands:**
```bash
systemctl status service
journalctl -u service
df -h
top/htop
netstat -tulpn
chmod/chown
find / -name filename
```

**Essential Skills:**
- Shell scripting
- SSH configuration
- Cron jobs
- Log analysis
- Performance tuning
- Backup strategies
- Troubleshooting

**Best Practices:**
- Keep system updated
- Use sudo instead of root
- Regular backups
- Monitor disk space
- Configure log rotation
- Implement security hardening
- Document changes
- Use configuration management

**Troubleshooting:**
- Check system logs
- Review service status
- Monitor resource usage
- Verify network connectivity
- Check file permissions
- Review recent changes""",
            "keywords": ["linux", "administration", "bash", "systemd", "server", "unix"],
            "created_by": "system"
        },
        {
            "technology_name": "Windows Administration",
            "category": TechnologyCategory.OPERATING_SYSTEM,
            "content": """**Windows Administration** covers Windows Server management tasks.

**Core Components:**
- Active Directory
- Group Policy
- DNS and DHCP
- File and Print Services
- IIS (Web Server)
- PowerShell automation
- Windows Update Services

**Common Tools:**
- Server Manager
- PowerShell
- AD Users and Computers
- Event Viewer
- Performance Monitor
- Remote Desktop

**PowerShell Examples:**
```powershell
Get-Service
Get-EventLog -LogName System
Get-ADUser -Filter *
Restart-Computer
Test-Connection hostname
```

**Best Practices:**
- Regular backups (Windows Server Backup)
- Implement GPOs properly
- Monitor event logs
- Keep systems updated (WSUS)
- Use PowerShell for automation
- Document AD structure
- Implement proper security
- Regular AD maintenance

**Troubleshooting:**
- Check Event Viewer logs
- Review service status
- Verify AD replication
- Test DNS resolution
- Check permissions
- Review GPO application""",
            "keywords": ["windows", "administration", "active directory", "powershell", "server"],
            "created_by": "system"
        },
        
        # Programming
        {
            "technology_name": "Python",
            "category": TechnologyCategory.PROGRAMMING,
            "content": """**Python** is a versatile programming language widely used in automation, scripting, and development.

**Common Use Cases:**
- Automation scripts
- Web applications (Flask, Django)
- Data analysis
- API development
- DevOps tooling
- System administration

**Key Concepts:**
- Virtual environments (venv, virtualenv)
- Package management (pip)
- Modules and imports
- Object-oriented programming
- Exception handling
- List comprehensions

**Common Commands:**
```bash
python3 --version
pip install package
pip freeze > requirements.txt
python3 -m venv venv
source venv/bin/activate
```

**Best Practices:**
- Use virtual environments
- Follow PEP 8 style guide
- Write docstrings
- Use type hints
- Handle exceptions properly
- Write unit tests
- Use requirements.txt
- Version control with Git

**Popular Libraries:**
- requests: HTTP library
- pandas: Data analysis
- flask/django: Web frameworks
- pytest: Testing framework
- paramiko: SSH library
- sqlalchemy: Database ORM

**Troubleshooting:**
- Check Python version
- Verify package installation
- Review import errors
- Check virtual environment
- Review stack traces
- Use debugger (pdb)""",
            "keywords": ["python", "programming", "scripting", "automation", "pip"],
            "created_by": "system"
        },
        
        # System Administration
        {
            "technology_name": "System Administration",
            "category": TechnologyCategory.SYSTEM_ADMINISTRATION,
            "content": """**System Administration** covers general practices for managing IT infrastructure.

**Core Responsibilities:**
- Server provisioning and maintenance
- User and access management
- Security implementation
- Backup and disaster recovery
- Performance monitoring
- Capacity planning
- Documentation

**Essential Skills:**
- Operating systems (Linux, Windows)
- Networking fundamentals
- Storage management
- Virtualization
- Security best practices
- Scripting and automation
- Troubleshooting methodology

**Key Tasks:**
- System patching and updates
- Resource monitoring
- Log management
- Incident response
- Change management
- Configuration management
- Automation implementation

**Best Practices:**
- Document everything
- Automate repetitive tasks
- Implement monitoring
- Regular backups and testing
- Security hardening
- Capacity planning
- Version control for configs
- Follow change management
- Keep skills updated

**Tools:**
- Monitoring: Zabbix, Prometheus, Nagios
- Automation: Ansible, Puppet, Chef
- Logging: ELK Stack, Graylog
- Backup: Veeam, Bacula
- Virtualization: VMware, KVM, Hyper-V
- Containerization: Docker, Kubernetes

**Troubleshooting Approach:**
1. Identify the problem
2. Gather information
3. Analyze data
4. Develop hypothesis
5. Test solution
6. Document resolution""",
            "keywords": ["sysadmin", "system administration", "infrastructure", "operations", "devops"],
            "created_by": "system"
        },
    ]
    
    # Add entries to knowledge base
    count = 0
    for entry in knowledge_entries:
        entry_id = kb_manager.add_knowledge(**entry)
        if entry_id:
            count += 1
            logger.info(f"Added: {entry['technology_name']}")
        else:
            logger.error(f"Failed to add: {entry['technology_name']}")
    
    logger.info(f"Successfully added {count}/{len(knowledge_entries)} knowledge entries")
    print(f"\n✅ Knowledge base populated with {count} technology entries!")


if __name__ == "__main__":
    populate_knowledge_base()
