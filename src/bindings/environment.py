"""
Isaac Sim 5.0 Environment

This module provides a unified environment interface for Isaac Sim 5.0.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from .simulation_app import SimulationApp
from .webrtc_client import WebRTCClient
from .rest_client import RESTClient

logger = logging.getLogger(__name__)


class IsaacSimEnvironment:
    """
    Unified Isaac Sim 5.0 environment.
    
    This class provides a unified interface for working with Isaac Sim 5.0,
    combining the SimulationApp, WebRTC client, and REST client.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Isaac Sim 5.0 environment.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.simulation_app = None
        self.webrtc_client = None
        self.rest_client = None
        self.is_initialized = False
        
        # Initialize components
        self._init_simulation_app()
        self._init_clients()
        
        logger.info("Isaac Sim 5.0 environment initialized")
    
    def _init_simulation_app(self):
        """Initialize the SimulationApp."""
        sim_config = self.config.get('simulation', {})
        self.simulation_app = SimulationApp(sim_config)
    
    def _init_clients(self):
        """Initialize WebRTC and REST clients."""
        host = self.config.get('host', '3.239.124.24')
        webrtc_port = self.config.get('webrtc_port', 8211)
        rest_port = self.config.get('rest_port', 3009)
        
        self.webrtc_client = WebRTCClient(host, webrtc_port)
        self.rest_client = RESTClient(host, rest_port)
    
    async def initialize(self) -> bool:
        """
        Initialize the environment.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            logger.info("Initializing Isaac Sim 5.0 environment...")
            
            # Start Isaac Sim 5.0
            if not self.simulation_app.start():
                logger.error("Failed to start Isaac Sim 5.0")
                return False
            
            # Connect to WebRTC
            if not await self.webrtc_client.connect():
                logger.warning("Failed to connect to WebRTC service")
            
            # Connect to REST API
            await self.rest_client.connect()
            
            self.is_initialized = True
            logger.info("Isaac Sim 5.0 environment initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize environment: {e}")
            return False
    
    async def cleanup(self):
        """Clean up the environment."""
        try:
            logger.info("Cleaning up Isaac Sim 5.0 environment...")
            
            if self.webrtc_client:
                await self.webrtc_client.disconnect()
            
            if self.rest_client:
                await self.rest_client.disconnect()
            
            if self.simulation_app:
                self.simulation_app.stop()
            
            self.is_initialized = False
            logger.info("Isaac Sim 5.0 environment cleaned up")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    async def start_simulation(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Start a simulation.
        
        Args:
            config: Simulation configuration
        
        Returns:
            True if simulation started successfully, False otherwise
        """
        if not self.is_initialized:
            if not await self.initialize():
                return False
        
        try:
            result = await self.rest_client.start_simulation(config)
            if 'error' not in result:
                logger.info("Simulation started successfully")
                return True
            else:
                logger.error(f"Failed to start simulation: {result['error']}")
                return False
        except Exception as e:
            logger.error(f"Error starting simulation: {e}")
            return False
    
    async def stop_simulation(self) -> bool:
        """
        Stop the current simulation.
        
        Returns:
            True if simulation stopped successfully, False otherwise
        """
        try:
            result = await self.rest_client.stop_simulation()
            if 'error' not in result:
                logger.info("Simulation stopped successfully")
                return True
            else:
                logger.error(f"Failed to stop simulation: {result['error']}")
                return False
        except Exception as e:
            logger.error(f"Error stopping simulation: {e}")
            return False
    
    async def get_simulation_status(self) -> Dict[str, Any]:
        """
        Get simulation status.
        
        Returns:
            Simulation status
        """
        return await self.rest_client.get_simulation_status()
    
    async def start_streaming(self) -> bool:
        """
        Start WebRTC streaming.
        
        Returns:
            True if streaming started successfully, False otherwise
        """
        try:
            return await self.webrtc_client.start_streaming()
        except Exception as e:
            logger.error(f"Error starting streaming: {e}")
            return False
    
    async def stop_streaming(self):
        """Stop WebRTC streaming."""
        try:
            await self.webrtc_client.stop_streaming()
        except Exception as e:
            logger.error(f"Error stopping streaming: {e}")
    
    async def get_status(self) -> Dict[str, Any]:
        """
        Get environment status.
        
        Returns:
            Dictionary containing status information
        """
        status = {
            'is_initialized': self.is_initialized,
            'simulation_app': self.simulation_app.get_status() if self.simulation_app else None,
            'webrtc_client': self.webrtc_client.get_status() if self.webrtc_client else None,
            'rest_client': self.rest_client.get_status_info() if self.rest_client else None
        }
        
        if self.is_initialized:
            try:
                status['simulation_status'] = await self.get_simulation_status()
            except Exception as e:
                status['simulation_status'] = {'error': str(e)}
        
        return status
    
    async def load_scene(self, scene_path: str) -> bool:
        """
        Load a scene.
        
        Args:
            scene_path: Path to scene file
        
        Returns:
            True if scene loaded successfully, False otherwise
        """
        try:
            result = await self.rest_client.load_scene(scene_path)
            if 'error' not in result:
                logger.info(f"Scene loaded successfully: {scene_path}")
                return True
            else:
                logger.error(f"Failed to load scene: {result['error']}")
                return False
        except Exception as e:
            logger.error(f"Error loading scene: {e}")
            return False
    
    async def get_scene_info(self) -> Dict[str, Any]:
        """
        Get current scene information.
        
        Returns:
            Scene information
        """
        return await self.rest_client.get_scene_info()
    
    async def get_entities(self) -> Dict[str, Any]:
        """
        Get simulation entities.
        
        Returns:
            Entity information
        """
        return await self.rest_client.get_entities()
    
    async def create_entity(self, entity_config: Dict[str, Any]) -> bool:
        """
        Create an entity.
        
        Args:
            entity_config: Entity configuration
        
        Returns:
            True if entity created successfully, False otherwise
        """
        try:
            result = await self.rest_client.create_entity(entity_config)
            if 'error' not in result:
                logger.info("Entity created successfully")
                return True
            else:
                logger.error(f"Failed to create entity: {result['error']}")
                return False
        except Exception as e:
            logger.error(f"Error creating entity: {e}")
            return False
    
    async def delete_entity(self, entity_id: str) -> bool:
        """
        Delete an entity.
        
        Args:
            entity_id: Entity ID
        
        Returns:
            True if entity deleted successfully, False otherwise
        """
        try:
            result = await self.rest_client.delete_entity(entity_id)
            if 'error' not in result:
                logger.info(f"Entity deleted successfully: {entity_id}")
                return True
            else:
                logger.error(f"Failed to delete entity: {result['error']}")
                return False
        except Exception as e:
            logger.error(f"Error deleting entity: {e}")
            return False
    
    def set_frame_callback(self, callback):
        """
        Set callback for frame data.
        
        Args:
            callback: Function to call when frame data is received
        """
        if self.webrtc_client:
            self.webrtc_client.set_frame_callback(callback)
    
    def set_audio_callback(self, callback):
        """
        Set callback for audio data.
        
        Args:
            callback: Function to call when audio data is received
        """
        if self.webrtc_client:
            self.webrtc_client.set_audio_callback(callback)
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
