#!/usr/bin/env python3
"""
Isaac Sim 5.0 Python Bindings - Example Runner

This script runs various examples for the Isaac Sim 5.0 Python bindings.
"""

import asyncio
import sys
import os
import argparse
import logging

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from bindings import IsaacSimEnvironment

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_basic_example():
    """Run the basic usage example."""
    logger.info("Running basic usage example...")
    
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
        logger.info("Environment initialized")
        
        # Get status
        status = await env.get_status()
        logger.info(f"Status: {status}")
        
        # Start streaming
        if await env.start_streaming():
            logger.info("Streaming started")
            logger.info(f"Stream URL: {env.webrtc_client.get_stream_url()}")
            
            # Run for 30 seconds
            await asyncio.sleep(30)
            
            await env.stop_streaming()
            logger.info("Streaming stopped")
        else:
            logger.error("Failed to start streaming")


async def run_g1_example():
    """Run the G1 training example."""
    logger.info("Running G1 training example...")
    
    # Import the G1 example
    from examples.g1_training import g1_training_example
    await g1_training_example()


async def run_status_check():
    """Run a status check."""
    logger.info("Running status check...")
    
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
        status = await env.get_status()
        logger.info("Environment Status:")
        for key, value in status.items():
            logger.info(f"  {key}: {value}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Isaac Sim 5.0 Python Bindings Examples')
    parser.add_argument('example', choices=['basic', 'g1', 'status'], 
                       help='Example to run')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("Isaac Sim 5.0 Python Bindings Examples")
    logger.info("=" * 50)
    
    if args.example == 'basic':
        asyncio.run(run_basic_example())
    elif args.example == 'g1':
        asyncio.run(run_g1_example())
    elif args.example == 'status':
        asyncio.run(run_status_check())
    
    logger.info("Example completed!")


if __name__ == "__main__":
    main()
