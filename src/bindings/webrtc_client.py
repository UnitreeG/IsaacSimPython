"""
Isaac Sim 5.0 WebRTC Client

This module provides a WebRTC client for streaming Isaac Sim 5.0 simulations.
"""

import asyncio
import websockets
import json
import logging
from typing import Dict, Any, Optional, Callable
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class WebRTCClient:
    """
    WebRTC client for Isaac Sim 5.0 streaming.
    
    This class provides functionality to connect to Isaac Sim 5.0's WebRTC
    streaming service and handle video/audio streams.
    """
    
    def __init__(self, host: str = "3.239.124.24", port: int = 8211):
        """
        Initialize the WebRTC client.
        
        Args:
            host: Isaac Sim 5.0 host address
            port: WebRTC port number
        """
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.webrtc_url = f"ws://{host}:{port}/streaming/webrtc"
        self.websocket = None
        self.is_connected = False
        self.on_frame_callback = None
        self.on_audio_callback = None
        
        logger.info(f"WebRTC client initialized for {self.base_url}")
    
    async def connect(self) -> bool:
        """
        Connect to Isaac Sim 5.0 WebRTC service.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            logger.info(f"Connecting to WebRTC service at {self.webrtc_url}")
            
            # Connect to WebRTC WebSocket
            self.websocket = await websockets.connect(self.webrtc_url)
            self.is_connected = True
            
            logger.info("WebRTC connection established")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to WebRTC service: {e}")
            self.is_connected = False
            return False
    
    async def disconnect(self):
        """Disconnect from WebRTC service."""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
        
        self.is_connected = False
        logger.info("WebRTC connection closed")
    
    async def send_message(self, message: Dict[str, Any]):
        """
        Send a message to the WebRTC service.
        
        Args:
            message: Message to send
        """
        if not self.is_connected or not self.websocket:
            logger.error("Not connected to WebRTC service")
            return
        
        try:
            await self.websocket.send(json.dumps(message))
            logger.debug(f"Sent message: {message}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
    
    async def receive_messages(self):
        """Receive and handle messages from WebRTC service."""
        if not self.is_connected or not self.websocket:
            logger.error("Not connected to WebRTC service")
            return
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self._handle_message(data)
                except json.JSONDecodeError:
                    logger.warning("Received non-JSON message")
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
        except websockets.exceptions.ConnectionClosed:
            logger.info("WebRTC connection closed")
            self.is_connected = False
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
    
    async def _handle_message(self, data: Dict[str, Any]):
        """
        Handle received WebRTC messages.
        
        Args:
            data: Received message data
        """
        message_type = data.get('type')
        
        if message_type == 'frame':
            if self.on_frame_callback:
                await self.on_frame_callback(data.get('frame'))
        elif message_type == 'audio':
            if self.on_audio_callback:
                await self.on_audio_callback(data.get('audio'))
        elif message_type == 'status':
            logger.info(f"Status update: {data.get('status')}")
        else:
            logger.debug(f"Received message type: {message_type}")
    
    def set_frame_callback(self, callback: Callable):
        """
        Set callback for frame data.
        
        Args:
            callback: Function to call when frame data is received
        """
        self.on_frame_callback = callback
    
    def set_audio_callback(self, callback: Callable):
        """
        Set callback for audio data.
        
        Args:
            callback: Function to call when audio data is received
        """
        self.on_audio_callback = callback
    
    async def start_streaming(self):
        """Start streaming from Isaac Sim 5.0."""
        if not self.is_connected:
            if not await self.connect():
                return False
        
        # Send start streaming message
        await self.send_message({
            'type': 'start_streaming',
            'format': 'webrtc'
        })
        
        logger.info("Started WebRTC streaming")
        return True
    
    async def stop_streaming(self):
        """Stop streaming from Isaac Sim 5.0."""
        if self.is_connected:
            await self.send_message({
                'type': 'stop_streaming'
            })
            logger.info("Stopped WebRTC streaming")
    
    def get_stream_url(self) -> str:
        """
        Get the WebRTC stream URL.
        
        Returns:
            WebRTC stream URL
        """
        return f"{self.base_url}/streaming/webrtc-client"
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the WebRTC client.
        
        Returns:
            Dictionary containing status information
        """
        return {
            'is_connected': self.is_connected,
            'host': self.host,
            'port': self.port,
            'base_url': self.base_url,
            'stream_url': self.get_stream_url()
        }
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.disconnect()
