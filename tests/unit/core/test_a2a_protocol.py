"""
Unit tests for a2a_protocol.py to cover missing functionality
"""
import sys
import os
import json
from unittest.mock import Mock, patch
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from a2a_protocol import A2AMessage, MessageType, A2AClient, get_agent_capabilities

def test_a2a_message_to_json():
    """Test the to_json method of A2AMessage"""
    message = A2AMessage(
        type=MessageType.REQUEST_RESEARCH_TASK.value,
        version="1.0",
        id="test-id",
        timestamp="2023-01-01T00:00:00Z",
        sender="sender-agent",
        receiver="receiver-agent",
        payload={"query": "test query"},
        metadata={"priority": "high"}
    )
    
    json_str = message.to_json()
    parsed = json.loads(json_str)
    
    assert parsed['type'] == MessageType.REQUEST_RESEARCH_TASK.value
    assert parsed['sender'] == "sender-agent"
    assert parsed['payload']['query'] == "test query"


def test_a2a_message_from_json():
    """Test the from_json method of A2AMessage"""
    json_str = json.dumps({
        "type": MessageType.RESPONSE_RESEARCH_RESULTS.value,
        "version": "1.0",
        "id": "test-id-2",
        "timestamp": "2023-01-01T00:00:00Z",
        "sender": "sender-agent-2",
        "receiver": "receiver-agent-2",
        "payload": {"results": "test results"},
        "metadata": {"priority": "normal"}
    })
    
    message = A2AMessage.from_json(json_str)
    
    assert message.type == MessageType.RESPONSE_RESEARCH_RESULTS.value
    assert message.sender == "sender-agent-2"
    assert message.payload["results"] == "test results"
    assert message.metadata["priority"] == "normal"


def test_a2a_client_shared_queue_creation():
    """Test A2AClient message queue creation"""
    client = A2AClient("test-agent")
    
    # Create a test message
    test_msg = A2AMessage(
        type=MessageType.REQUEST_RESEARCH_TASK.value,
        version="1.0",
        id="test-id",
        timestamp="2023-01-01T00:00:00Z",
        sender="sender",
        receiver="receiver",
        payload={"query": "test"}
    )
    
    # Remove any existing queue for a clean test
    if hasattr(A2AClient, 'message_queue'):
        delattr(A2AClient, 'message_queue')
    
    # Call send_message to create the queue
    result = client.send_message("test-receiver", test_msg)
    
    # Verify the queue was created and message was added
    assert result is True
    assert hasattr(A2AClient, 'message_queue')
    assert len(A2AClient.message_queue) == 1
    assert A2AClient.message_queue[0].type == MessageType.REQUEST_RESEARCH_TASK.value


def test_a2a_client_shared_queue_append():
    """Test A2AClient message queue appending to existing queue"""
    client = A2AClient("test-agent")
    
    # Create first test message
    first_msg = A2AMessage(
        type=MessageType.REQUEST_RESEARCH_TASK.value,
        version="1.0",
        id="test-id-1",
        timestamp="2023-01-01T00:00:00Z",
        sender="sender",
        receiver="receiver",
        payload={"query": "test1"}
    )
    
    # Create second test message
    second_msg = A2AMessage(
        type=MessageType.RESPONSE_RESEARCH_RESULTS.value,
        version="1.0",
        id="test-id-2",
        timestamp="2023-01-01T00:00:00Z",
        sender="sender",
        receiver="receiver",
        payload={"results": "test2"}
    )
    
    # Remove any existing queue for a clean test
    if hasattr(A2AClient, 'message_queue'):
        delattr(A2AClient, 'message_queue')
    
    # Add first message (creates queue)
    client.send_message("test-receiver", first_msg)
    
    # Add second message (appends to existing queue)
    client.send_message("test-receiver", second_msg)
    
    # Verify both messages are in the queue
    assert hasattr(A2AClient, 'message_queue')
    assert len(A2AClient.message_queue) == 2
    assert A2AClient.message_queue[0].payload["query"] == "test1"
    assert A2AClient.message_queue[1].payload["results"] == "test2"


def test_get_agent_capabilities():
    """Test the get_agent_capabilities function"""
    capabilities = get_agent_capabilities(
        agent_id="test-agent",
        name="Test Agent", 
        description="Test agent for testing",
        supported_types=[MessageType.REQUEST_RESEARCH_TASK.value]
    )
    
    assert capabilities["@context"] == "https://a2a-protocol.org/context.jsonld"
    assert capabilities["id"] == "test-agent"
    assert capabilities["name"] == "Test Agent"
    assert capabilities["description"] == "Test agent for testing"
    
    # Check supported message types structure
    assert len(capabilities["supportedMessageTypes"]) == 1
    assert capabilities["supportedMessageTypes"][0]["type"] == MessageType.REQUEST_RESEARCH_TASK.value
    assert capabilities["supportedMessageTypes"][0]["direction"] == "incoming"
    
    # Check endpoints
    assert capabilities["endpoints"]["message"] == "/a2a/message"
    assert capabilities["endpoints"]["capabilities"] == "/a2a/capabilities"
    assert capabilities["endpoints"]["status"] == "/a2a/status"