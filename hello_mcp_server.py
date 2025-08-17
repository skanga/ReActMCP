#!/usr/bin/env python3
"""
Simple Hello MCP Server
A basic MCP server implementation that provides greeting and utility tools.
"""

import asyncio
import json
import sys
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

class HelloMCPServer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.protocol_version = "2024-11-05"
        self.server_info = {
            "name": "hello-mcp-server",
            "version": "1.0.0"
        }
        
        # Available tools
        self.tools = {
            "say_hello": {
                "name": "say_hello",
                "description": "Say hello to someone with an optional message",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the person to greet"
                        },
                        "message": {
                            "type": "string",
                            "description": "Optional custom message",
                            "default": "Nice to meet you!"
                        }
                    },
                    "required": ["name"]
                }
            },
            "get_time": {
                "name": "get_time",
                "description": "Get the current date and time",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "format": {
                            "type": "string",
                            "description": "Time format (iso, readable, timestamp)",
                            "enum": ["iso", "readable", "timestamp"],
                            "default": "readable"
                        }
                    }
                }
            },
            "echo": {
                "name": "echo",
                "description": "Echo back the provided message",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to echo back"
                        }
                    },
                    "required": ["message"]
                }
            },
            "calculate": {
                "name": "calculate",
                "description": "Perform basic arithmetic calculations",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')"
                        }
                    },
                    "required": ["expression"]
                }
            }
        }
    
    async def handle_initialize(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {
                "protocolVersion": self.protocol_version,
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": self.server_info
            }
        }
    
    async def handle_tools_list(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools list request"""
        tools_list = list(self.tools.values())
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {
                "tools": tools_list
            }
        }
    
    async def handle_tools_call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call request"""
        params = request.get("params", {})
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }
        
        try:
            result = await self._execute_tool(tool_name, arguments)
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32603,
                    "message": f"Tool execution failed: {str(e)}"
                }
            }
    
    async def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Execute the specified tool with given arguments"""
        if tool_name == "say_hello":
            name = arguments.get("name", "World")
            message = arguments.get("message", "Nice to meet you!")
            return f"Hello, {name}! {message}"
        
        elif tool_name == "get_time":
            format_type = arguments.get("format", "readable")
            now = datetime.now()
            
            if format_type == "iso":
                return now.isoformat()
            elif format_type == "timestamp":
                return str(int(now.timestamp()))
            else:  # readable
                return now.strftime("%Y-%m-%d %H:%M:%S")
        
        elif tool_name == "echo":
            message = arguments.get("message", "")
            return f"Echo: {message}"
        
        elif tool_name == "calculate":
            expression = arguments.get("expression", "")
            try:
                # Safe evaluation of basic math expressions
                # Only allow numbers, basic operators, and parentheses
                allowed_chars = set("0123456789+-*/().,\t\n ")
                if not all(c in allowed_chars for c in expression):
                    return "Error: Invalid characters in expression"
                
                result = eval(expression)
                return f"{expression} = {result}"
            except Exception as e:
                return f"Error calculating '{expression}': {str(e)}"
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming JSON-RPC request"""
        method = request.get("method")
        
        if method == "initialize":
            return await self.handle_initialize(request)
        elif method == "tools/list":
            return await self.handle_tools_list(request)
        elif method == "tools/call":
            return await self.handle_tools_call(request)
        else:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }
    
    async def run(self):
        """Main server loop - reads from stdin and writes to stdout"""
        self.logger.info("Hello MCP Server starting...")
        
        # Read from stdin line by line
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # Parse JSON request
                try:
                    request = json.loads(line)
                except json.JSONDecodeError as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    continue
                
                # Handle request
                response = await self.handle_request(request)
                
                if response:
                    print(json.dumps(response), flush=True)
                
            except EOFError:
                break
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
        
        self.logger.info("Hello MCP Server shutting down...")


async def main():
    """Main entry point"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)]  # Log to stderr to avoid interfering with stdout
    )
    
    server = HelloMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())