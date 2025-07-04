"""
Isaac Sim 5.0 REST Client

This module provides a REST client for interacting with Isaac Sim 5.0's REST API.
"""

import aiohttp
import json
import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class RESTClient:
    """
    REST client for Isaac Sim 5.0 API.
    
    This class provides functionality to interact with Isaac Sim 5.0's REST API
    for controlling simulations, getting status, and managing resources.
    """
    
    def __init__(self, host: str = "3.239.124.24", port: int = 3009):
        """
        Initialize the REST client.
        
        Args:
            host: Isaac Sim 5.0 host address
            port: REST API port number
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.session = None
        
        logger.info(f"REST client initialized for {self.base_url}")
    
    async def connect(self):
        """Create HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession()
            logger.info("REST client session created")
    
    async def disconnect(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("REST client session closed")
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to Isaac Sim 5.0 REST API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request data (for POST/PUT requests)
        
        Returns:
            Response data
        """
        if not self.session:
            await self.connect()
        
        url = urljoin(self.base_url, endpoint)
        
        try:
            async with self.session.request(method, url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"HTTP {response.status}: {await response.text()}")
                    return {'error': f'HTTP {response.status}'}
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return {'error': str(e)}
    
    async def get_version(self) -> Dict[str, Any]:
        """
        Get Isaac Sim 5.0 version information.
        
        Returns:
            Version information
        """
        return await self._make_request('GET', '/version')
    
    async def get_health(self) -> Dict[str, Any]:
        """
        Get Isaac Sim 5.0 health status.
        
        Returns:
            Health status
        """
        return await self._make_request('GET', '/health')
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get Isaac Sim 5.0 status.
        
        Returns:
            Status information
        """
        return await self._make_request('GET', '/status')
    
    async def start_simulation(self, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Start a simulation.
        
        Args:
            config: Simulation configuration
        
        Returns:
            Start result
        """
        return await self._make_request('POST', '/simulation/start', config or {})
    
    async def stop_simulation(self) -> Dict[str, Any]:
        """
        Stop the current simulation.
        
        Returns:
            Stop result
        """
        return await self._make_request('POST', '/simulation/stop')
    
    async def pause_simulation(self) -> Dict[str, Any]:
        """
        Pause the current simulation.
        
        Returns:
            Pause result
        """
        return await self._make_request('POST', '/simulation/pause')
    
    async def resume_simulation(self) -> Dict[str, Any]:
        """
        Resume the current simulation.
        
        Returns:
            Resume result
        """
        return await self._make_request('POST', '/simulation/resume')
    
    async def get_simulation_status(self) -> Dict[str, Any]:
        """
        Get simulation status.
        
        Returns:
            Simulation status
        """
        return await self._make_request('GET', '/simulation/status')
    
    async def load_scene(self, scene_path: str) -> Dict[str, Any]:
        """
        Load a scene.
        
        Args:
            scene_path: Path to scene file
        
        Returns:
            Load result
        """
        return await self._make_request('POST', '/scene/load', {'path': scene_path})
    
    async def get_scene_info(self) -> Dict[str, Any]:
        """
        Get current scene information.
        
        Returns:
            Scene information
        """
        return await self._make_request('GET', '/scene/info')
    
    async def set_camera(self, camera_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set camera configuration.
        
        Args:
            camera_config: Camera configuration
        
        Returns:
            Set result
        """
        return await self._make_request('POST', '/camera/set', camera_config)
    
    async def get_camera_info(self) -> Dict[str, Any]:
        """
        Get camera information.
        
        Returns:
            Camera information
        """
        return await self._make_request('GET', '/camera/info')
    
    async def set_lighting(self, lighting_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set lighting configuration.
        
        Args:
            lighting_config: Lighting configuration
        
        Returns:
            Set result
        """
        return await self._make_request('POST', '/lighting/set', lighting_config)
    
    async def get_lighting_info(self) -> Dict[str, Any]:
        """
        Get lighting information.
        
        Returns:
            Lighting information
        """
        return await self._make_request('GET', '/lighting/info')
    
    async def get_physics_info(self) -> Dict[str, Any]:
        """
        Get physics information.
        
        Returns:
            Physics information
        """
        return await self._make_request('GET', '/physics/info')
    
    async def set_physics_config(self, physics_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Set physics configuration.
        
        Args:
            physics_config: Physics configuration
        
        Returns:
            Set result
        """
        return await self._make_request('POST', '/physics/config', physics_config)
    
    async def get_entities(self) -> Dict[str, Any]:
        """
        Get simulation entities.
        
        Returns:
            Entity information
        """
        return await self._make_request('GET', '/entities')
    
    async def create_entity(self, entity_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an entity.
        
        Args:
            entity_config: Entity configuration
        
        Returns:
            Creation result
        """
        return await self._make_request('POST', '/entities/create', entity_config)
    
    async def delete_entity(self, entity_id: str) -> Dict[str, Any]:
        """
        Delete an entity.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            Deletion result
        """
        return await self._make_request('DELETE', f'/entities/{entity_id}')
    
    async def get_logs(self, level: str = "INFO", limit: int = 100) -> Dict[str, Any]:
        """
        Get simulation logs.
        
        Args:
            level: Log level
            limit: Number of log entries to return
        
        Returns:
            Log entries
        """
        return await self._make_request('GET', f'/logs?level={level}&limit={limit}')
    
    def get_status_info(self) -> Dict[str, Any]:
        """
        Get the current status of the REST client.
        
        Returns:
            Dictionary containing status information
        """
        return {
            'host': self.host,
            'port': self.port,
            'base_url': self.base_url,
            'session_active': self.session is not None
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
