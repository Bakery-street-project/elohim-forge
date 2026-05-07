# Elohim Forge — PRIMAX AI Edition

> **WATERMARK**: PRIMAX-AI-ELOHIM-BSP-2025  

## 🌟 Support This Project

**[💙 Become a Sponsor](https://github.com/sponsors/kilisan)** — Get advanced backends and priority CLI support!

See [PREMIUM.md](PREMIUM.md) and [SPONSORS.md](SPONSORS.md) for details.

> **License**: Proprietary — Bakery Street Project  
> **Copyright**: © 2024-2025 Bakery Street Project. All Rights Reserved.

---

## 🌟 Overview

**Elohim Forge** is a next-generation CLI oracle and development platform powered by **PRIMAX AI** — a neuromorphic intelligence system featuring multi-agent orchestration, MCP (Model Context Protocol) integration, and AST-based codebase analysis.

Built for the **Code Elohim** universe, combining lore-driven development with enterprise-grade AI tooling.

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/bakery-street-project/elohim-forge.git
cd elohim-forge/cli

# Install dependencies
pip install -e . --break-system-packages

# Install nest-asyncio (for async orchestration)
pip install nest-asyncio --break-system-packages

# Install RestrictedPython (for sandboxing)
pip install RestrictedPython --break-system-packages

# Install PRIMAX AI components
cd /home/kilisan/primax-ai
pip install -e .
```

### Setup Backend

Choose **one** of the following free backends:

#### Option 1: NVIDIA NIM (Recommended - Free Tier)
```bash
# Sign up at https://developer.nvidia.com
# Get API key from https://build.nvidia.com/nim
export NIM_API_KEY="your-nvidia-api-key"
export NIM_MODEL="meta/llama-3.1-8b-instruct"
```

#### Option 2: Local Ollama (PRIMAX)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull PRIMAX model
ollama pull primax-dragon-coder:latest

# Set backend
export PRIMAX_API_KEY="local"
export PRIMAX_BACKEND="primax"
```

#### Option 3: Gemini API
```bash
export GEMINI_API_KEY="your-gemini-key"
```

#### Option 4: OpenAI API
```bash
export OPENAI_API_KEY="your-openai-key"
```

### Launch

```bash
# Run the CLI
cd /home/kilisan/elohim-forge/cli
python elohim.py --help
```

---

## 🎮 Desktop Linux App (npm + MCP Server)

### Prerequisites

```bash
# Install Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install MCP SDK
npm install -g @modelcontextprotocol/sdk

# Install PRIMAX MCP server
npm install -g @primax-ai/mcp-server
```

### Build Desktop App

```bash
# Clone and build
cd /home/kilisan/elohim-forge

# Install Electron
npm install electron --save-dev

# Install dependencies
npm install

# Build for Linux
npm run build:linux

# Output: dist/elohim-linux-x64/elohim
```

### Package.json Scripts

```json
{
  "scripts": {
    "start": "electron .",
    "build:linux": "electron-builder --linux",
    "build:mac": "electron-builder --mac",
    "build:win": "electron-builder --win",
    "dev": "electron . --enable-logging"
  }
}
```

### Run Desktop App

```bash
# Development mode
npm start

# Production
./dist/elohim-linux-x64/elohim
```

---

## 🔧 MCP Server Integration

### Start MCP Server

```bash
# Using Python
python -m src.mcp_server.primax_mcp_server

# Using npm
npx @primax-ai/mcp-server

# Using Docker
docker run -p 8000:8000 primax-ai/mcp-server:latest
```

### MCP Tools Available

| Tool | Description |
|------|-------------|
| `primax_chat` | Chat with PRIMAX AI |
| `primax_analyze_repo` | Analyze GitHub repository |
| `primax_brain_analysis` | Neuromorphic brain analysis |
| `primax_code_scan` | Scan local codebase |

### Configure MCP Client

```json
{
  "mcpServers": {
    "primax": {
      "command": "python",
      "args": ["-m", "src.mcp_server.primax_mcp_server"],
      "cwd": "/home/kilisan/primax-ai"
    }
  }
}
```

---

## 📦 Sponsorship Tiers

### 🥉 Bronze Tier — $10/month
- Access to basic features
- Community support
- Monthly newsletter
- Name in CONTRIBUTORS.md

### 🥈 Silver Tier — $50/month
- All Bronze benefits
- Priority issue resolution
- Early access to features
- Custom lore generation
- Name in SPONSORS.md

### 🥇 Gold Tier — $200/month
- All Silver benefits
- Direct access to maintainers
- Feature requests prioritized
- Private deployment assistance
- Custom agent training
- Name in PATRONS.md

### 💎 Platinum Tier — $1000/month
- All Gold benefits
- White-label licensing option
- SLA guarantee (99.9% uptime)
- Dedicated support channel
- Onboarding consultation
- Co-branding opportunities
- Executive sponsor listing

### 🏆 Enterprise Tier — Custom
- All Platinum benefits
- Unlimited private deployments
- Custom SLA and support
- Dedicated engineering team
- On-premise installation
- Compliance certifications
- Source code escrow

### Cryptocurrency Donations

```
Bitcoin (BTC):  bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh
Ethereum (ETH): 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7
```

---

## 📄 Licensing

### Proprietary License

**Copyright © 2024-2025 Bakery Street Project**

All rights reserved. No part of this software may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the copyright holder.

**Exceptions:**
- Open-source components retain their original licenses
- Third-party libraries follow their respective licenses
- Documentation is CC-BY-NC-SA 4.0

### Component Licenses

| Component | License |
|-----------|---------|
| PRIMAX AI Core | Proprietary - BSP-2025 |
| Elohim CLI | Proprietary - BSD-3-Clause |
| Nexus Adapter | MIT |
| Codebase Scanner | Apache 2.0 |
| MCP Server | MIT |
| Desktop App | GPL-3.0 |

---

## 🔒 Copyright & Watermarking

### Watermark Format

All source files include the following watermark:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PRIMAX AI - [COMPONENT]                                    ║
║                                                                               ║
║  Copyright (c) 2024-2025 Bakery Street Project - ALL RIGHTS RESERVED         ║
║  WATERMARK: PRIMAX-AI-[COMPONENT]-BSP-2025                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Watermarked Components

- ✅ PRIMAX-AI-TUI-BSP-2025
- ✅ PRIMAX-AI-MCP-BSP-2025
- ✅ PRIMAX-AI-NEXUS-BSP-2025
- ✅ PRIMAX-AI-SCANNER-BSP-2025
- ✅ PRIMAX-AI-GRAPHQL-BSP-2025
- ✅ PRIMAX-AI-WEBHOOK-BSP-2025
- ✅ PRIMAX-AI-WORKFLOW-BSP-2025
- ✅ PRIMAX-AI-ELOHIM-BSP-2025

---

## 🌐 Free Tier Deployment

### Local Deployment (Free)

```bash
# Using Ollama (CPU/GPU)
ollama pull primax-dragon-coder:latest
ollama run primax-dragon-coder:latest
```

### Cloud Deployment (Free Tier)

| Platform | Free Tier | Limitations |
|----------|-----------|-------------|
| **NVIDIA NIM** | ✅ Yes | Rate limits apply |
| **Google Colab** | ✅ Yes | Session timeout |
| **RunPod Community** | ✅ Yes | Spot instances |
| **GitHub Codespaces** | ❌ No | GPU deprecated |

### Cost Breakdown

| Resource | Cost | Notes |
|----------|------|-------|
| **Local CPU** | $0 | Slow but functional |
| **Local GPU** | $0 | Requires hardware |
| **NVIDIA NIM** | $0 | Free tier available |
| **RunPod** | $0.34/hr | RTX 4090 (24GB) |
| **Lambda Labs** | $1.29/hr | A10 (24GB) |

---

## 🎯 Usage Examples

### PRIMAX AI Commands

```bash
# Check system status
elohim primax status

# Multi-agent orchestration
elohim primax nexus "analyze codebase architecture"

# Codebase scanning
elohim primax scan --path .

# MCP server query
elohim primax mcp "Explain PRIMAX architecture"
```

### GitHub Integration

```bash
# Analyze organization
elohim github org bakery-street-project

# Analyze repository
elohim github analyze owner/repo

# Create pull request
elohim github pr --title "Feature" --body "Description"
```

### Lore & Battle

```bash
# Query lore
elohim lore ask "What are the 13 shards?"

# List factions
elohim faction list

# Simulate battle
elohim battle simulate

# Generate roadmap
elohim forge cluster --save
```

---

## 📊 Performance Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **Codebase Scan** | 1.8M lines / 5s | ✅ Excellent |
| **Nexus Orchestration** | <1s per agent | ✅ Excellent |
| **Ollama Inference** | 2-4 tokens/sec | ⚠️ CPU-limited |
| **GitHub API** | 20 repos / 10s | ✅ Excellent |
| **MCP Response** | <1s | ✅ Excellent |

---

## 🤝 Contributing

### For Sponsors

- Direct access to maintainers
- Feature request prioritization
- Private deployment support

### For Community

- Issue reporting
- Documentation improvements
- Bug fixes
- Feature suggestions

### Code of Conduct

- Respect all contributors
- Follow project conventions
- Maintain watermark headers
- Document all changes

---

## 📞 Support

### Priority Support (Sponsors)

- Direct Discord access
- 24-hour response time
- Private consultation

### Community Support

- GitHub Issues
- Documentation
- Community Discord

---

## 🔄 Updates

### Version 0.1.0 (2026-05-06)

- ✅ PRIMAX AI integration
- ✅ MCP server support
- ✅ Nexus multi-agent system
- ✅ Codebase scanner
- ✅ GitHub integration
- ✅ Desktop Linux app
- ✅ Sponsorship tiers
- ✅ Watermarking system

---

## 🏷️ Trademarks

- **PRIMAX AI** is a trademark of Bakery Street Project
- **Code Elohim** is a trademark of Bakery Street Project
- **Nexus** is a trademark of Bakery Street Project

---

## 📝 License Notice

```
Copyright (c) 2024-2025 Bakery Street Project

Licensed under the Proprietary License.
All rights reserved.

WATERMARK: PRIMAX-AI-ELOHIM-BSP-2025
```

---

**Last Updated**: 2026-05-06  
**Maintainer**: Bakery Street Project  
**Watermark**: PRIMAX-AI-ELOHIM-BSP-2025  
**Status**: Production Ready ✅
