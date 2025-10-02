"""
Enhanced A2A Protocol Implementation for Multi-Agent Research System with Tool Support
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class MessageType(Enum):
    REQUEST_RESEARCH_TASK = "request:research:task"
    RESPONSE_RESEARCH_RESULTS = "response:research:results"
    REQUEST_FACTCHECK_VERIFY = "request:factcheck:verify"
    RESPONSE_FACTCHECK_RESULTS = "response:factcheck:results"
    REQUEST_USE_TOOL = "request:use-tool"
    RESPONSE_TOOL_RESULT = "response:tool-result"


@dataclass
class A2AMessage:
    """A2A Protocol Message Structure"""
    type: str
    version: str
    id: str
    timestamp: str
    sender: str
    receiver: str
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        """Convert message to JSON string"""
        return json.dumps(asdict(self))
    
    @classmethod
    def from_json(cls, json_str: str) -> 'A2AMessage':
        """Create message from JSON string"""
        data = json.loads(json_str)
        return cls(**data)

    @classmethod
    def create_message(cls, msg_type: MessageType, sender: str, receiver: str, 
                      payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> 'A2AMessage':
        """Create a new A2A message with required fields"""
        return cls(
            type=msg_type.value,
            version="1.0",
            id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            sender=sender,
            receiver=receiver,
            payload=payload,
            metadata=metadata or {}
        )


class A2AClient:
    """Basic A2A client for sending messages between agents"""
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
    
    def send_message(self, receiver: str, message: A2AMessage) -> bool:
        """
        Send message to another agent - in a real implementation this would make HTTP calls
        For this demo, we'll use a mock implementation that stores messages in a queue
        """
        # In a real implementation, this would be an HTTP POST to receiver's /a2a/message endpoint
        print(f"A2A Client {self.agent_id} sending message to {receiver}: {message.type}")
        # For demo purposes, we'll store the message in a shared queue
        if hasattr(A2AClient, 'message_queue'):
            A2AClient.message_queue.append(message)
        else:
            A2AClient.message_queue = [message]
        return True


def get_agent_capabilities(agent_id: str, name: str, description: str, supported_types: list) -> Dict[str, Any]:
    """Generate A2A agent capabilities in JSON-LD format"""
    return {
        "@context": "https://a2a-protocol.org/context.jsonld",
        "id": agent_id,
        "name": name,
        "version": "1.0.0",
        "description": description,
        "supportedMessageTypes": [
            {
                "type": msg_type,
                "direction": "incoming" if msg_type.startswith("request") else "outgoing",
                "schema": f"schema-reference-{msg_type}"
            } for msg_type in supported_types
        ],
        "endpoints": {
            "message": "/a2a/message",
            "capabilities": "/a2a/capabilities",
            "status": "/a2a/status"
        }
    }