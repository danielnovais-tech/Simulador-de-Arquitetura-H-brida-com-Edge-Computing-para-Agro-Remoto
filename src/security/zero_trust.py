"""
Security System - NSE3000 Security Policies and Zero-Trust Architecture
"""
import hashlib
import secrets
import time
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from loguru import logger


class SecurityLevel(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    CRITICAL = "critical"


class AccessAction(Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"


@dataclass
class SecurityPrincipal:
    """Represents a user, service, or device"""
    id: str
    name: str
    type: str  # user, service, device
    security_level: SecurityLevel
    permissions: Set[str] = field(default_factory=set)
    active_sessions: List[str] = field(default_factory=list)


@dataclass
class SecurityPolicy:
    """Defines access control policy"""
    name: str
    resource_pattern: str
    allowed_principals: List[str]
    allowed_actions: List[AccessAction]
    conditions: Dict = field(default_factory=dict)
    enabled: bool = True


@dataclass
class AuditLog:
    """Security audit log entry"""
    timestamp: float
    principal_id: str
    resource: str
    action: AccessAction
    result: bool
    reason: str = ""


class ZeroTrustSecurityManager:
    """
    Implements Zero-Trust security architecture
    - Never trust, always verify
    - Least privilege access
    - Microsegmentation
    """
    
    def __init__(self):
        self.principals: Dict[str, SecurityPrincipal] = {}
        self.policies: List[SecurityPolicy] = []
        self.audit_logs: List[AuditLog] = []
        self.sessions: Dict[str, Dict] = {}
        self.max_session_age = 3600  # 1 hour
        
        # Initialize default policies
        self._initialize_default_policies()
    
    def _initialize_default_policies(self):
        """Initialize default zero-trust policies"""
        # Policy 1: Edge nodes can only read sensor data
        self.policies.append(SecurityPolicy(
            name="edge_sensor_read",
            resource_pattern="sensors/*",
            allowed_principals=["edge-node-*"],
            allowed_actions=[AccessAction.READ]
        ))
        
        # Policy 2: Control system can write to actuators
        self.policies.append(SecurityPolicy(
            name="control_actuator_write",
            resource_pattern="actuators/*",
            allowed_principals=["control-system"],
            allowed_actions=[AccessAction.WRITE]
        ))
        
        # Policy 3: Admin full access
        self.policies.append(SecurityPolicy(
            name="admin_full_access",
            resource_pattern="*",
            allowed_principals=["admin"],
            allowed_actions=[AccessAction.READ, AccessAction.WRITE, AccessAction.EXECUTE, AccessAction.DELETE]
        ))
    
    def register_principal(self, principal: SecurityPrincipal):
        """Register a new security principal"""
        self.principals[principal.id] = principal
        logger.info(f"Registered principal: {principal.name} ({principal.type})")
    
    def create_session(self, principal_id: str) -> Optional[str]:
        """Create authenticated session for principal"""
        if principal_id not in self.principals:
            logger.warning(f"Unknown principal: {principal_id}")
            return None
        
        # Generate secure session token
        session_id = secrets.token_urlsafe(32)
        
        self.sessions[session_id] = {
            "principal_id": principal_id,
            "created_at": time.time(),
            "last_access": time.time()
        }
        
        self.principals[principal_id].active_sessions.append(session_id)
        logger.info(f"Created session for {principal_id}")
        
        return session_id
    
    def validate_session(self, session_id: str) -> bool:
        """Validate session is active and not expired"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        age = time.time() - session["created_at"]
        
        if age > self.max_session_age:
            self.revoke_session(session_id)
            return False
        
        # Update last access
        session["last_access"] = time.time()
        return True
    
    def revoke_session(self, session_id: str):
        """Revoke an active session"""
        if session_id in self.sessions:
            session = self.sessions.pop(session_id)
            principal_id = session["principal_id"]
            
            if principal_id in self.principals:
                principal = self.principals[principal_id]
                if session_id in principal.active_sessions:
                    principal.active_sessions.remove(session_id)
            
            logger.info(f"Revoked session {session_id}")
    
    def check_access(
        self,
        principal_id: str,
        resource: str,
        action: AccessAction,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Zero-trust access check
        - Verify principal exists
        - Verify session if provided
        - Check policies
        - Log access attempt
        """
        # Validate principal
        if principal_id not in self.principals:
            self._log_access(principal_id, resource, action, False, "Unknown principal")
            return False
        
        # Validate session if provided
        if session_id and not self.validate_session(session_id):
            self._log_access(principal_id, resource, action, False, "Invalid session")
            return False
        
        # Check policies
        principal = self.principals[principal_id]
        
        for policy in self.policies:
            if not policy.enabled:
                continue
            
            # Check if policy applies to this principal
            if not self._matches_principal(principal_id, policy.allowed_principals):
                continue
            
            # Check if policy applies to this resource
            if not self._matches_resource(resource, policy.resource_pattern):
                continue
            
            # Check if action is allowed
            if action in policy.allowed_actions:
                self._log_access(principal_id, resource, action, True, f"Matched policy: {policy.name}")
                return True
        
        self._log_access(principal_id, resource, action, False, "No matching policy")
        return False
    
    def _matches_principal(self, principal_id: str, patterns: List[str]) -> bool:
        """Check if principal matches any pattern"""
        for pattern in patterns:
            if pattern == principal_id:
                return True
            if pattern.endswith("*") and principal_id.startswith(pattern[:-1]):
                return True
        return False
    
    def _matches_resource(self, resource: str, pattern: str) -> bool:
        """Check if resource matches pattern"""
        if pattern == "*":
            return True
        if pattern.endswith("*") and resource.startswith(pattern[:-1]):
            return True
        return resource == pattern
    
    def _log_access(
        self,
        principal_id: str,
        resource: str,
        action: AccessAction,
        result: bool,
        reason: str
    ):
        """Log access attempt for audit"""
        log = AuditLog(
            timestamp=time.time(),
            principal_id=principal_id,
            resource=resource,
            action=action,
            result=result,
            reason=reason
        )
        
        self.audit_logs.append(log)
        
        if not result:
            logger.warning(
                f"Access denied: {principal_id} -> {resource} ({action.value}): {reason}"
            )
    
    def get_audit_logs(self, principal_id: Optional[str] = None, limit: int = 100) -> List[Dict]:
        """Get audit logs, optionally filtered by principal"""
        logs = self.audit_logs[-limit:]
        
        if principal_id:
            logs = [log for log in logs if log.principal_id == principal_id]
        
        return [
            {
                "timestamp": log.timestamp,
                "principal": log.principal_id,
                "resource": log.resource,
                "action": log.action.value,
                "result": "allowed" if log.result else "denied",
                "reason": log.reason
            }
            for log in logs
        ]
    
    def get_security_status(self) -> Dict:
        """Get overall security status"""
        recent_logs = self.audit_logs[-100:]
        denied_count = sum(1 for log in recent_logs if not log.result)
        
        return {
            "total_principals": len(self.principals),
            "active_sessions": len(self.sessions),
            "active_policies": sum(1 for p in self.policies if p.enabled),
            "total_policies": len(self.policies),
            "recent_access_attempts": len(recent_logs),
            "recent_denials": denied_count,
            "denial_rate": (denied_count / len(recent_logs) * 100) if recent_logs else 0
        }


class CertificateManager:
    """Manages TLS/SSL certificates for secure communication"""
    
    def __init__(self):
        self.certificates: Dict[str, Dict] = {}
    
    def generate_certificate(self, entity_id: str, validity_days: int = 365) -> str:
        """Generate self-signed certificate for entity"""
        # Simplified certificate generation
        cert_data = f"{entity_id}:{time.time()}:{validity_days}"
        cert_hash = hashlib.sha256(cert_data.encode()).hexdigest()
        
        self.certificates[entity_id] = {
            "hash": cert_hash,
            "created_at": time.time(),
            "expires_at": time.time() + (validity_days * 86400),
            "revoked": False
        }
        
        logger.info(f"Generated certificate for {entity_id}")
        return cert_hash
    
    def validate_certificate(self, entity_id: str, cert_hash: str) -> bool:
        """Validate certificate"""
        if entity_id not in self.certificates:
            return False
        
        cert = self.certificates[entity_id]
        
        if cert["revoked"]:
            logger.warning(f"Certificate for {entity_id} has been revoked")
            return False
        
        if time.time() > cert["expires_at"]:
            logger.warning(f"Certificate for {entity_id} has expired")
            return False
        
        return cert["hash"] == cert_hash
    
    def revoke_certificate(self, entity_id: str):
        """Revoke certificate"""
        if entity_id in self.certificates:
            self.certificates[entity_id]["revoked"] = True
            logger.info(f"Revoked certificate for {entity_id}")
