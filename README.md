# Isaac Sim 5.0 Python Bindings

A clean, focused project for working with Isaac Sim 5.0 Python bindings and API.

## 🚀 Overview

This project provides a streamlined environment for:
- Isaac Sim 5.0 Python API development
- WebRTC streaming integration
- Simulation app development
- Python bindings testing and debugging

## 📁 Project Structure

```
IsaacSimPython/
├── src/                    # Source code
│   ├── bindings/          # Python bindings
│   ├── examples/          # Example scripts
│   └── utils/             # Utility functions
├── tests/                 # Test files
├── docs/                  # Documentation
├── config/                # Configuration files
└── scripts/               # Build and setup scripts
```

## 🔧 Setup

### Prerequisites
- Isaac Sim 5.0 built from source
- Python 3.11+
- Remote AWS instance with Isaac Sim 5.0

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd IsaacSimPython

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🌐 Remote Connection

This project is designed to work with the remote Isaac Sim 5.0 instance:

- **Host**: 3.239.124.24
- **WebRTC**: http://3.239.124.24:8211
- **REST API**: http://3.239.124.24:3009
- **SSH Key**: ~/g1-stabilization-key.pem

## 🎯 Features

- ✅ Isaac Sim 5.0 Python bindings
- ✅ WebRTC streaming support
- ✅ Simulation app development
- ✅ Clean API interface
- ✅ Example implementations

## 📚 Usage

### Basic Isaac Sim 5.0 Import
```python
import sys
import os

# Add Isaac Sim 5.0 paths
isaac_paths = [
    '/workspace/isaac-sim-5.0',
    '/workspace/isaac-sim-5.0/_build/linux-x86_64/release',
    '/workspace/isaac-sim-5.0/_build/linux-x86_64/release/exts'
]

for path in isaac_paths:
    if path not in sys.path and os.path.exists(path):
        sys.path.insert(0, path)

# Import Isaac Sim 5.0
from isaacsim import SimulationApp
```

### WebRTC Streaming
```python
# Start Isaac Sim 5.0 with WebRTC
app = SimulationApp({
    'headless': True,
    'livestream': 'webrtc',
    'webrtc_port': 8211,
    'rest_port': 3009
})
```

## 🔍 Development

### Running Tests
```bash
python -m pytest tests/
```

### Building Documentation
```bash
cd docs && make html
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the documentation in `docs/`
- Review example implementations in `src/examples/`
