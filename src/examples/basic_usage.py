"""
Basic Isaac Sim 5.0 Usage Example

This example demonstrates basic usage of the Isaac Sim 5.0 Python bindings.
"""

import asyncio
import logging
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.bindings import IsaacSimEnvironment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def basic_usage_example():
    """Basic usage example for Isaac Sim 5.0."""
    
    # Configuration for Isaac Sim 5.0
    config = {
        'host': '3.239.124.24',
        'webrtc_port': 8211,
        'rest_port': 3009,
        'simulation': {
            'headless': True,
            'livestream': 'webrtc'
        }
    }
    
    # Create Isaac Sim 5.0 environment
    logger.info("Creating Isaac Sim 5.0 environment...")
    env = IsaacSimEnvironment(config)
    
    try:
        # Initialize the environment
        logger.info("Initializing environment...")
        if not await env.initialize():
            logger.error("Failed to initialize environment")
            return
        
        # Get environment status
        status = await env.get_status()
        logger.info(f"Environment status: {status}")
        
        # Start WebRTC streaming
        logger.info("Starting WebRTC streaming...")
        if await env.start_streaming():
            logger.info("WebRTC streaming started")
            logger.info(f"Stream URL: {env.webrtc_client.get_stream_url()}")
        else:
            logger.warning("Failed to start WebRTC streaming")
        
        # Get simulation status
        sim_status = await env.get_simulation_status()
        logger.info(f"Simulation status: {sim_status}")
        
        # Get scene information
        scene_info = await env.get_scene_info()
        logger.info(f"Scene info: {scene_info}")
        
        # Get entities
        entities = await env.get_entities()
        logger.info(f"Entities: {entities}")
        
        # Keep running for a while to observe
        logger.info("Running for 30 seconds...")
        await asyncio.sleep(30)
        
        # Stop streaming
        logger.info("Stopping WebRTC streaming...")
        await env.stop_streaming()
        
        logger.info("Basic usage example completed successfully!")
        
    except Exception as e:
        logger.error(f"Error in basic usage example: {e}")
    
    finally:
        # Clean up
        await env.cleanup()


async def simulation_control_example():
    """Example of controlling Isaac Sim 5.0 simulations."""
    
    config = {
        'host': '3.239.124.24',
        'webrtc_port': 8211,
        'rest_port': 3009,
        'simulation': {
            'headless': True,
            'livestream': 'webrtc'
        }
    }
    
    async with IsaacSimEnvironment(config) as env:
        logger.info("Simulation control example started")
        
        # Start a simulation
        sim_config = {
            'scene': 'default',
            'physics_dt': 0.01,
            'rendering_dt': 0.016
        }
        
        if await env.start_simulation(sim_config):
            logger.info("Simulation started successfully")
            
            # Get simulation status
            status = await env.get_simulation_status()
            logger.info(f"Simulation status: {status}")
            
            # Run for a while
            await asyncio.sleep(10)
            
            # Stop simulation
            if await env.stop_simulation():
                logger.info("Simulation stopped successfully")
            else:
                logger.error("Failed to stop simulation")
        else:
            logger.error("Failed to start simulation")


async def streaming_example():
    """Example of WebRTC streaming with Isaac Sim 5.0."""
    
    config = {
        'host': '3.239.124.24',
        'webrtc_port': 8211,
        'rest_port': 3009,
        'simulation': {
            'headless': True,
            'livestream': 'webrtc'
        }
    }
    
    async with IsaacSimEnvironment(config) as env:
        logger.info("Streaming example started")
        
        # Set up frame callback
        def on_frame(frame_data):
            logger.info(f"Received frame: {len(frame_data)} bytes")
        
        env.set_frame_callback(on_frame)
        
        # Start streaming
        if await env.start_streaming():
            logger.info("Streaming started")
            logger.info(f"Stream URL: {env.webrtc_client.get_stream_url()}")
            
            # Run for a while to receive frames
            await asyncio.sleep(30)
            
            # Stop streaming
            await env.stop_streaming()
            logger.info("Streaming stopped")
        else:
            logger.error("Failed to start streaming")


def main():
    """Main function to run examples."""
    logger.info("Isaac Sim 5.0 Basic Usage Examples")
    logger.info("=" * 50)
    
    # Run basic usage example
    logger.info("Running basic usage example...")
    asyncio.run(basic_usage_example())
    
    # Run simulation control example
    logger.info("Running simulation control example...")
    asyncio.run(simulation_control_example())
    
    # Run streaming example
    logger.info("Running streaming example...")
    asyncio.run(streaming_example())
    
    logger.info("All examples completed!")


if __name__ == "__main__":
    main()
