"""Knowledge base manager for storing and retrieving technology documentation."""

import uuid
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from models import KnowledgeEntry, TechnologyCategory
from database import get_db

logger = logging.getLogger(__name__)


class KnowledgeBaseManager:
    """Manager for knowledge base operations."""
    
    # Technology keywords mapping
    TECHNOLOGY_KEYWORDS = {
        # Orchestration
        "ansible": ["ansible", "playbook", "role", "automation", "configuration management"],
        "kubernetes": ["kubernetes", "k8s", "pod", "deployment", "service", "ingress", "helm", "kubectl"],
        "openshift": ["openshift", "oc", "route", "project", "buildconfig"],
        "puppet": ["puppet", "manifest", "module", "hiera", "facter"],
        
        # Containerization
        "docker": ["docker", "container", "image", "dockerfile", "registry"],
        "docker-swarm": ["swarm", "stack", "service", "overlay network"],
        "docker-compose": ["docker-compose", "compose file", "yml", "services"],
        
        # Infrastructure as Code
        "terraform": ["terraform", "tf", "provider", "resource", "state", "plan", "apply"],
        
        # CI/CD
        "argo-cd": ["argocd", "gitops", "sync", "application"],
        "gitlab-ci": ["gitlab", "ci/cd", "pipeline", ".gitlab-ci.yml", "runner", "job"],
        
        # Monitoring & Logging
        "elk": ["elasticsearch", "logstash", "kibana", "elk stack", "beats"],
        "zabbix": ["zabbix", "agent", "monitoring", "trigger", "item"],
        "grafana": ["grafana", "dashboard", "panel", "datasource"],
        "prometheus": ["prometheus", "promql", "metrics", "alert"],
        
        # Databases
        "mysql": ["mysql", "mariadb", "sql", "database", "query"],
        "postgresql": ["postgresql", "postgres", "psql", "pg"],
        
        # Networking
        "cisco": ["cisco", "router", "switch", "ios", "vlan"],
        "mikrotik": ["mikrotik", "routeros", "winbox"],
        "keenetic": ["keenetic", "router", "wifi"],
        
        # Operating Systems
        "linux": ["linux", "bash", "shell", "systemd", "ssh", "permissions"],
        "windows": ["windows", "powershell", "active directory", "iis"],
        
        # Programming
        "python": ["python", "pip", "virtualenv", "script", "module"],
    }
    
    def __init__(self):
        """Initialize knowledge base manager."""
        pass
    
    def add_knowledge(
        self,
        technology_name: str,
        category: TechnologyCategory,
        content: str,
        keywords: List[str],
        created_by: str
    ) -> Optional[str]:
        """
        Add new knowledge entry to database.
        
        Args:
            technology_name: Name of the technology
            category: Technology category
            content: Documentation content
            keywords: Search keywords
            created_by: Creator identifier
            
        Returns:
            Entry ID if successful, None otherwise
        """
        try:
            with get_db() as db:
                entry_id = str(uuid.uuid4())
                
                entry = KnowledgeEntry(
                    entry_id=entry_id,
                    technology_name=technology_name,
                    category=category,
                    content=content,
                    keywords=keywords,
                    created_by=created_by
                )
                
                db.add(entry)
                db.commit()
                
                logger.info(f"Added knowledge entry for {technology_name}")
                return entry_id
                
        except Exception as e:
            logger.error(f"Failed to add knowledge entry: {e}")
            return None
    
    def update_knowledge(
        self,
        entry_id: str,
        content: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> bool:
        """
        Update existing knowledge entry.
        
        Args:
            entry_id: Knowledge entry ID
            content: New content (if updating)
            keywords: New keywords (if updating)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with get_db() as db:
                entry = db.query(KnowledgeEntry).filter(
                    KnowledgeEntry.entry_id == entry_id
                ).first()
                
                if not entry:
                    logger.warning(f"Knowledge entry {entry_id} not found")
                    return False
                
                if content:
                    entry.content = content
                if keywords:
                    entry.keywords = keywords
                
                entry.version += 1
                entry.updated_at = datetime.utcnow()
                
                db.commit()
                logger.info(f"Updated knowledge entry {entry_id}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to update knowledge entry: {e}")
            return False
    
    def search_knowledge(self, query: str, max_results: int = 3) -> str:
        """
        Search knowledge base and return relevant context.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            Formatted knowledge context string
        """
        query_lower = query.lower()
        
        # Identify relevant technologies from query
        identified_techs = []
        for tech, keywords in self.TECHNOLOGY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    identified_techs.append(tech)
                    break
        
        if not identified_techs:
            return ""
        
        # Retrieve knowledge entries
        try:
            with get_db() as db:
                entries = []
                
                for tech in identified_techs[:max_results]:
                    entry = db.query(KnowledgeEntry).filter(
                        KnowledgeEntry.technology_name.ilike(f"%{tech}%")
                    ).first()
                    
                    if entry:
                        entries.append(entry)
                
                # Format context
                if not entries:
                    return ""
                
                context_parts = []
                for entry in entries:
                    context_parts.append(
                        f"## {entry.technology_name} ({entry.category.value})\n{entry.content}"
                    )
                
                return "\n\n".join(context_parts)
                
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return ""
    
    def get_all_technologies(self) -> List[Dict[str, Any]]:
        """
        Get list of all technologies in knowledge base.
        
        Returns:
            List of technology dictionaries
        """
        try:
            with get_db() as db:
                entries = db.query(KnowledgeEntry).all()
                
                return [
                    {
                        'entry_id': entry.entry_id,
                        'technology_name': entry.technology_name,
                        'category': entry.category.value,
                        'version': entry.version,
                        'updated_at': entry.updated_at.isoformat()
                    }
                    for entry in entries
                ]
                
        except Exception as e:
            logger.error(f"Error retrieving technologies: {e}")
            return []
    
    def identify_technologies(self, query: str) -> List[str]:
        """
        Identify technologies mentioned in a query.
        
        Args:
            query: User query
            
        Returns:
            List of identified technology names
        """
        query_lower = query.lower()
        identified = []
        
        for tech, keywords in self.TECHNOLOGY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in query_lower:
                    identified.append(tech)
                    break
        
        return identified


# Global knowledge base manager instance
_kb_manager: Optional[KnowledgeBaseManager] = None


def get_kb_manager() -> KnowledgeBaseManager:
    """Get or create knowledge base manager instance."""
    global _kb_manager
    if _kb_manager is None:
        _kb_manager = KnowledgeBaseManager()
    return _kb_manager
