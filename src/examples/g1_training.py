"""
G1 Training Example with Isaac Sim 5.0

This example demonstrates how to use Isaac Sim 5.0 for G1 robot training.
"""

import asyncio
import logging
import sys
import os
import subprocess
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.bindings import IsaacSimEnvironment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def g1_training_example():
    """G1 training example using Isaac Sim 5.0."""
    
    # Configuration for Isaac Sim 5.0 with G1 training
    config = {
        'host': '3.239.124.24',
        'webrtc_port': 8211,
        'rest_port': 3009,
        'simulation': {
            'headless': True,
            'livestream': 'webrtc'
        }
    }
    
    logger.info("G1 Training Example with Isaac Sim 5.0")
    logger.info("=" * 50)
    
    # Create Isaac Sim 5.0 environment
    async with IsaacSimEnvironment(config) as env:
        logger.info("Isaac Sim 5.0 environment initialized")
        
        # Get environment status
        status = await env.get_status()
        logger.info(f"Environment status: {status}")
        
        # Start WebRTC streaming for monitoring
        logger.info("Starting WebRTC streaming for training monitoring...")
        if await env.start_streaming():
            logger.info("WebRTC streaming started")
            logger.info(f"Monitor training at: {env.webrtc_client.get_stream_url()}")
        else:
            logger.warning("Failed to start WebRTC streaming")
        
        # Set up frame callback for monitoring
        def on_training_frame(frame_data):
            logger.debug(f"Training frame received: {len(frame_data)} bytes")
        
        env.set_frame_callback(on_training_frame)
        
        # Start G1 training
        logger.info("Starting G1 training...")
        
        # Change to G1 directory
        g1_dir = '/workspace/g1_23dof_locomotion_isaac'
        if os.path.exists(g1_dir):
            os.chdir(g1_dir)
            logger.info(f"Changed to G1 directory: {os.getcwd()}")
            
            # Start G1 training with Isaac Sim 5.0
            training_cmd = [
                'python3', 'scripts/rsl_rl/train.py',
                '--task=Isaac-Velocity-Flat-G1-v0',
                '--headless',
                '--num_envs=16'
            ]
            
            logger.info(f"Training command: {' '.join(training_cmd)}")
            logger.info("Starting G1 training process...")
            
            try:
                # Start training process
                process = subprocess.Popen(
                    training_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                logger.info(f"G1 training started with PID: {process.pid}")
                logger.info("Training is now running in the background")
                logger.info("Monitor progress via WebRTC stream")
                
                # Monitor training for a while
                logger.info("Monitoring training for 60 seconds...")
                await asyncio.sleep(60)
                
                # Check if process is still running
                if process.poll() is None:
                    logger.info("Training is still running")
                    logger.info("You can continue monitoring or stop the process")
                else:
                    logger.info("Training process completed")
                    stdout, stderr = process.communicate()
                    logger.info(f"Training output: {stdout[:500]}...")
                    if stderr:
                        logger.warning(f"Training errors: {stderr[:500]}...")
                
            except Exception as e:
                logger.error(f"Error starting G1 training: {e}")
        else:
            logger.error(f"G1 directory not found: {g1_dir}")
        
        # Stop streaming
        logger.info("Stopping WebRTC streaming...")
        await env.stop_streaming()
        
        logger.info("G1 training example completed!")


async def g1_training_monitor():
    """Monitor G1 training with Isaac Sim 5.0."""
    
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
        logger.info("G1 Training Monitor")
        logger.info("=" * 30)
        
        # Start streaming
        if await env.start_streaming():
            logger.info("WebRTC streaming started for monitoring")
            logger.info(f"Monitor URL: {env.webrtc_client.get_stream_url()}")
            
            # Monitor for a longer period
            logger.info("Monitoring training for 5 minutes...")
            await asyncio.sleep(300)
            
            # Stop streaming
            await env.stop_streaming()
            logger.info("Monitoring completed")
        else:
            logger.error("Failed to start streaming for monitoring")


def check_g1_environment():
    """Check if G1 training environment is ready."""
    logger.info("Checking G1 training environment...")
    
    # Check G1 directory
    g1_dir = '/workspace/g1_23dof_locomotion_isaac'
    if os.path.exists(g1_dir):
        logger.info(f"✅ G1 directory found: {g1_dir}")
        
        # Check training script
        train_script = os.path.join(g1_dir, 'scripts/rsl_rl/train.py')
        if os.path.exists(train_script):
            logger.info(f"✅ Training script found: {train_script}")
        else:
            logger.error(f"❌ Training script not found: {train_script}")
    else:
        logger.error(f"❌ G1 directory not found: {g1_dir}")
    
    # Check Isaac Sim 5.0
    isaac_path = '/workspace/isaac-sim-5.0/_build/linux-x86_64/release/omni.isaac.sim'
    if os.path.exists(isaac_path):
        logger.info(f"✅ Isaac Sim 5.0 found: {isaac_path}")
    else:
        logger.error(f"❌ Isaac Sim 5.0 not found: {isaac_path}")
    
    # Check Isaac Lab
    isaac_lab_path = '/workspace/isaac-lab-2.2'
    if os.path.exists(isaac_lab_path):
        logger.info(f"✅ Isaac Lab found: {isaac_lab_path}")
    else:
        logger.error(f"❌ Isaac Lab not found: {isaac_lab_path}")


def main():
    """Main function to run G1 training examples."""
    logger.info("G1 Training with Isaac Sim 5.0")
    logger.info("=" * 50)
    
    # Check environment
    check_g1_environment()
    
    # Run G1 training example
    logger.info("Running G1 training example...")
    asyncio.run(g1_training_example())
    
    # Run monitoring example
    logger.info("Running G1 training monitor...")
    asyncio.run(g1_training_monitor())
    
    logger.info("G1 training examples completed!")


if __name__ == "__main__":
    main()
