"""
Isaac Sim 5.0 SimulationApp

This module provides the main SimulationApp class for interacting with Isaac Sim 5.0.
"""

import os
import sys
import subprocess
import time
import threading
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class SimulationApp:
    """
    Isaac Sim 5.0 SimulationApp
    
    This class provides a Python interface to Isaac Sim 5.0's simulation engine.
    It handles the startup, configuration, and management of Isaac Sim 5.0 instances.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Isaac Sim 5.0 SimulationApp.
        
        Args:
            config: Configuration dictionary for Isaac Sim 5.0
        """
        self.config = config or {}
        self.process = None
        self.is_running = False
        self.webrtc_port = self.config.get('webrtc_port', 8211)
        self.rest_port = self.config.get('rest_port', 3009)
        self.headless = self.config.get('headless', True)
        self.livestream = self.config.get('livestream', 'webrtc')
        
        # Set up Isaac Sim 5.0 paths
        self._setup_isaac_paths()
        
        # Set up environment variables
        self._setup_environment()
        
        logger.info("Isaac Sim 5.0 SimulationApp initialized")
    
    def _setup_isaac_paths(self):
        """Set up Isaac Sim 5.0 Python paths."""
        isaac_paths = [
            '/workspace/isaac-sim-5.0',
            '/workspace/isaac-sim-5.0/_build/linux-x86_64/release',
            '/workspace/isaac-sim-5.0/_build/linux-x86_64/release/exts',
            '/workspace/isaac-sim-5.0/_build/linux-x86_64/release/omni.isaac.sim'
        ]
        
        for path in isaac_paths:
            if path not in sys.path and os.path.exists(path):
                sys.path.insert(0, path)
                logger.debug(f"Added Isaac Sim path: {path}")
    
    def _setup_environment(self):
        """Set up environment variables for Isaac Sim 5.0."""
        env_vars = {
            'HEADLESS': '1' if self.headless else '0',
            'OMNI_LIVESTREAM': self.livestream,
            'OMNI_WEBRTC_PORT_HTTP': str(self.webrtc_port),
            'OMNI_WEBRTC_PORT_UDP': '49100',
            'OMNI_KIT_ALLOW_ROOT': '1',
            'ACCEPT_EULA': 'Y',
            'PRIVACY_CONSENT': 'Y',
            'ISAAC_SIM_PATH': '/workspace/isaac-sim-5.0',
            'ISAAC_LAB_PATH': '/workspace/isaac-lab-2.2'
        }
        
        for key, value in env_vars.items():
            os.environ[key] = value
            logger.debug(f"Set environment variable: {key}={value}")
    
    def start(self) -> bool:
        """
        Start Isaac Sim 5.0.
        
        Returns:
            True if Isaac Sim 5.0 started successfully, False otherwise
        """
        if self.is_running:
            logger.warning("Isaac Sim 5.0 is already running")
            return True
        
        try:
            # Check if Isaac Sim 5.0 is already running
            if self._is_isaac_running():
                logger.info("Isaac Sim 5.0 is already running")
                self.is_running = True
                return True
            
            # Start Isaac Sim 5.0
            isaac_cmd = [
                '/workspace/isaac-sim-5.0/_build/linux-x86_64/release/omni.isaac.sim',
                '--headless' if self.headless else '',
                '--livestream', self.livestream,
                '--webrtc-port', str(self.webrtc_port),
                '--rest-port', str(self.rest_port)
            ]
            
            # Remove empty arguments
            isaac_cmd = [arg for arg in isaac_cmd if arg]
            
            logger.info(f"Starting Isaac Sim 5.0 with command: {' '.join(isaac_cmd)}")
            
            # Start Isaac Sim 5.0 in background
            self.process = subprocess.Popen(
                isaac_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=os.environ.copy()
            )
            
            # Wait a moment for startup
            time.sleep(2)
            
            # Check if process started successfully
            if self.process.poll() is None:
                self.is_running = True
                logger.info("Isaac Sim 5.0 started successfully")
                return True
            else:
                logger.error("Isaac Sim 5.0 failed to start")
                return False
                
        except Exception as e:
            logger.error(f"Error starting Isaac Sim 5.0: {e}")
            return False
    
    def _is_isaac_running(self) -> bool:
        """Check if Isaac Sim 5.0 is already running."""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'isaac-sim'],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def stop(self):
        """Stop Isaac Sim 5.0."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
        
        self.is_running = False
        logger.info("Isaac Sim 5.0 stopped")
    
    def restart(self) -> bool:
        """
        Restart Isaac Sim 5.0.
        
        Returns:
            True if restart successful, False otherwise
        """
        self.stop()
        time.sleep(1)
        return self.start()
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of Isaac Sim 5.0.
        
        Returns:
            Dictionary containing status information
        """
        status = {
            'is_running': self.is_running,
            'webrtc_port': self.webrtc_port,
            'rest_port': self.rest_port,
            'headless': self.headless,
            'livestream': self.livestream
        }
        
        if self.process:
            status['pid'] = self.process.pid
            status['returncode'] = self.process.poll()
        
        return status
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
    
    def __del__(self):
        """Cleanup on deletion."""
        if self.is_running:
            self.stop()
