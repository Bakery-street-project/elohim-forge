"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    PRIMAX AI - Elohim Integration                             ║
║                                                                               ║
║  Copyright (c) 2024-2025 Bakery Street Project - ALL RIGHTS RESERVED         ║
║  WATERMARK: PRIMAX-AI-ELOHIM-BSP-2025                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import httpx
import subprocess
import json
import asyncio
import nest_asyncio
from typing import Optional
from .base import BaseBackend
from ..config import load_config

class PrimaxMCPBackend(BaseBackend):
    """PRIMAX AI MCP backend for elohim-forge"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self._base_url = base_url.rstrip("/")
    
    @property
    def name(self) -> str:
        return "PRIMAX-MCP"
    
    def chat(self, messages: list[dict], system: str = "") -> str:
        """Chat via PRIMAX MCP server"""
        try:
            # Try to use PRIMAX MCP server
            resp = httpx.post(
                f"{self.base_url}/mcp/chat",
                json={
                    "messages": messages,
                    "system": system,
                    "model": "primax-dragon-coder:latest"
                },
                timeout=30.0
            )
            if resp.status_code == 200:
                return resp.json().get("content", "")
        except Exception:
            pass
        
        # Fallback to local Ollama
        return self._ollama_fallback(messages, system)
    
    def _ollama_fallback(self, messages: list[dict], system: str) -> str:
        """Fallback to local Ollama"""
        try:
            full_prompt = ""
            if system:
                full_prompt += f"System: {system}\n"
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                if role == "system":
                    full_prompt += f"System: {content}\n"
                else:
                    full_prompt += f"{role.capitalize()}: {content}\n"
            
            full_prompt += "Assistant:"
            
            process = subprocess.Popen(
                ["ollama", "run", "primax-dragon-coder:latest"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, _ = process.communicate(input=full_prompt, timeout=30)
            return stdout.strip()
        except Exception as e:
            return f"Error: {str(e)}"

class PrimaxNexusBackend(BaseBackend):
    """PRIMAX Nexus multi-agent backend"""
    
    @property
    def name(self) -> str:
        return "PRIMAX-Nexus"
    
    def chat(self, messages: list[dict], system: str = "") -> str:
        """Use PRIMAX Nexus for multi-agent orchestration"""
        try:
            import sys
            sys.path.insert(0, '/home/kilisan/primax-ai/src')
            from nexus_adapter import create_primax_agents
            
            adapter = create_primax_agents()
            
            # Extract last user message
            last_msg = ""
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    last_msg = msg.get("content", "")
                    break
            
            # Route to appropriate agent
            if "code" in last_msg.lower() or "implement" in last_msg.lower():
                agent = "dragon-coder"
            elif "analyze" in last_msg.lower() or "review" in last_msg.lower():
                agent = "scout-agent"
            elif "brain" in last_msg.lower() or "system" in last_msg.lower():
                agent = "wisdom-brain"
            else:
                agent = "wisdom-brain"
            
            # Run async in sync context
            nest_asyncio.apply()
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                adapter.dispatch_task(agent, last_msg)
            )
            
            return result.get("result", str(result))
        except Exception as e:
            return f"Nexus Error: {str(e)}"

class PrimaxScannerBackend(BaseBackend):
    """PRIMAX codebase scanner backend"""
    
    @property
    def name(self) -> str:
        return "PRIMAX-Scanner"
    
    def chat(self, messages: list[dict], system: str = "") -> str:
        """Scan codebase and provide analysis"""
        try:
            import sys
            sys.path.insert(0, '/home/kilisan/primax-ai/src')
            from codebase_scanner import scan_repository
            
            last_msg = ""
            for msg in reversed(messages):
                if msg.get("role") == "user":
                    last_msg = msg.get("content", "")
                    break
            
            if "scan" in last_msg.lower() or "analyze" in last_msg.lower():
                result = scan_repository(".")
                return (
                    f"Codebase Analysis:\n"
                    f"  Files: {len(result.files)}\n"
                    f"  Lines: {result.total_lines}\n"
                    f"  Functions: {result.total_functions}\n"
                    f"  Classes: {result.total_classes}\n"
                    f"  Languages: {dict(result.languages)}"
                )
        except Exception as e:
            return f"Scanner Error: {str(e)}"
        
        return "Please specify what to scan or analyze."
