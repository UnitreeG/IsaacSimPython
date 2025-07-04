"""
Tests for Isaac Sim 5.0 Python Bindings

This module contains tests for the Isaac Sim 5.0 Python bindings.
"""

import pytest
import asyncio
import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from bindings import SimulationApp, WebRTCClient, RESTClient, IsaacSimEnvironment


class TestSimulationApp:
    """Test SimulationApp class."""
    
    def test_init(self):
        """Test SimulationApp initialization."""
        app = SimulationApp()
        assert app is not None
        assert app.config is not None
        assert app.webrtc_port == 8211
        assert app.rest_port == 3009
        assert app.headless is True
    
    def test_config(self):
        """Test SimulationApp with custom config."""
        config = {
            'webrtc_port': 9000,
            'rest_port': 4000,
            'headless': False
        }
        app = SimulationApp(config)
        assert app.webrtc_port == 9000
        assert app.rest_port == 4000
        assert app.headless is False
    
    def test_get_status(self):
        """Test get_status method."""
        app = SimulationApp()
        status = app.get_status()
        assert isinstance(status, dict)
        assert 'is_running' in status
        assert 'webrtc_port' in status
        assert 'rest_port' in status


class TestWebRTCClient:
    """Test WebRTCClient class."""
    
    def test_init(self):
        """Test WebRTCClient initialization."""
        client = WebRTCClient()
        assert client is not None
        assert client.host == "3.239.124.24"
        assert client.port == 8211
        assert client.base_url == "http://3.239.124.24:8211"
    
    def test_custom_host_port(self):
        """Test WebRTCClient with custom host and port."""
        client = WebRTCClient("localhost", 8080)
        assert client.host == "localhost"
        assert client.port == 8080
        assert client.base_url == "http://localhost:8080"
    
    def test_get_status(self):
        """Test get_status method."""
        client = WebRTCClient()
        status = client.get_status()
        assert isinstance(status, dict)
        assert 'is_connected' in status
        assert 'host' in status
        assert 'port' in status
        assert 'base_url' in status
        assert 'stream_url' in status


class TestRESTClient:
    """Test RESTClient class."""
    
    def test_init(self):
        """Test RESTClient initialization."""
        client = RESTClient()
        assert client is not None
        assert client.host == "3.239.124.24"
        assert client.port == 3009
        assert client.base_url == "http://3.239.124.24:3009"
    
    def test_custom_host_port(self):
        """Test RESTClient with custom host and port."""
        client = RESTClient("localhost", 8080)
        assert client.host == "localhost"
        assert client.port == 8080
        assert client.base_url == "http://localhost:8080"
    
    def test_get_status_info(self):
        """Test get_status_info method."""
        client = RESTClient()
        status = client.get_status_info()
        assert isinstance(status, dict)
        assert 'host' in status
        assert 'port' in status
        assert 'base_url' in status
        assert 'session_active' in status


class TestIsaacSimEnvironment:
    """Test IsaacSimEnvironment class."""
    
    def test_init(self):
        """Test IsaacSimEnvironment initialization."""
        env = IsaacSimEnvironment()
        assert env is not None
        assert env.config is not None
        assert env.simulation_app is not None
        assert env.webrtc_client is not None
        assert env.rest_client is not None
        assert env.is_initialized is False
    
    def test_custom_config(self):
        """Test IsaacSimEnvironment with custom config."""
        config = {
            'host': 'localhost',
            'webrtc_port': 9000,
            'rest_port': 4000
        }
        env = IsaacSimEnvironment(config)
        assert env.config == config
        assert env.webrtc_client.host == 'localhost'
        assert env.webrtc_client.port == 9000
        assert env.rest_client.port == 4000


@pytest.mark.asyncio
async def test_environment_async_context():
    """Test IsaacSimEnvironment async context manager."""
    config = {
        'host': 'localhost',
        'webrtc_port': 9000,
        'rest_port': 4000
    }
    
    async with IsaacSimEnvironment(config) as env:
        assert env is not None
        assert env.is_initialized is True


def test_imports():
    """Test that all modules can be imported."""
    from bindings import SimulationApp, WebRTCClient, RESTClient, IsaacSimEnvironment
    assert SimulationApp is not None
    assert WebRTCClient is not None
    assert RESTClient is not None
    assert IsaacSimEnvironment is not None


if __name__ == "__main__":
    pytest.main([__file__])
