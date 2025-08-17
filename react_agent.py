import asyncio
import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
import re

from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROQ = "groq"
    OPENROUTER = "openrouter"

@dataclass
class MCPTool:
    name: str
    description: str
    parameters: Dict[str, Any]

@dataclass
class ReActStep:
    thought: str
    action: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None

class LLMInterface(ABC):
    @abstractmethod
    async def chat(self, messages: List[BaseMessage]) -> str:
        pass

class OpenAILLM(LLMInterface):
    def __init__(self, model: str = "gpt-4", api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            openai_api_base=base_url
        )
    
    async def chat(self, messages: List[BaseMessage]) -> str:
        response = await self.llm.ainvoke(messages)
        return response.content

class AnthropicLLM(LLMInterface):
    def __init__(self, model: str = "claude-3-sonnet-20240229", api_key: Optional[str] = None):
        self.llm = ChatAnthropic(
            model=model,
            anthropic_api_key=api_key
        )
    
    async def chat(self, messages: List[BaseMessage]) -> str:
        response = await self.llm.ainvoke(messages)
        return response.content

class GoogleLLM(LLMInterface):
    def __init__(self, model: str = "gemini-pro", api_key: Optional[str] = None):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key
        )
    
    async def chat(self, messages: List[BaseMessage]) -> str:
        response = await self.llm.ainvoke(messages)
        return response.content

class GroqLLM(LLMInterface):
    def __init__(self, model: str = "mixtral-8x7b-32768", api_key: Optional[str] = None):
        from groq import AsyncGroq
        self.client = AsyncGroq(api_key=api_key)
        self.model = model
    
    async def chat(self, messages: List[BaseMessage]) -> str:
        groq_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                groq_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                groq_messages.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                groq_messages.append({"role": "system", "content": msg.content})
        
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=groq_messages
        )
        return response.choices[0].message.content

class OpenRouterLLM(LLMInterface):
    def __init__(self, model: str = "anthropic/claude-3-sonnet", api_key: Optional[str] = None):
        self.llm = ChatOpenAI(
            model=model,
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
    
    async def chat(self, messages: List[BaseMessage]) -> str:
        response = await self.llm.ainvoke(messages)
        return response.content

class MCPClient:
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.process = None
        self.tools = []
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Start the MCP server process"""
        try:
            self.process = await asyncio.create_subprocess_exec(
                *self.server_command,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Initialize connection
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "clientInfo": {
                        "name": "react-agent",
                        "version": "1.0.0"
                    }
                }
            }
            
            await self._send_request(init_request)
            response = await self._receive_response()
            
            if "error" in response:
                raise Exception(f"MCP initialization failed: {response['error']}")
            
            # Get available tools
            await self._fetch_tools()
            
            self.logger.info(f"MCP client started with {len(self.tools)} tools available")
            
        except Exception as e:
            self.logger.error(f"Failed to start MCP client: {e}")
            raise
    
    async def _send_request(self, request: Dict[str, Any]):
        """Send a JSON-RPC request to the MCP server"""
        if not self.process or not self.process.stdin:
            raise Exception("MCP server not started")
        
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
    
    async def _receive_response(self) -> Dict[str, Any]:
        """Receive a JSON-RPC response from the MCP server"""
        if not self.process or not self.process.stdout:
            raise Exception("MCP server not started")
        
        line = await self.process.stdout.readline()
        if not line:
            raise Exception("MCP server disconnected")
        
        return json.loads(line.decode().strip())
    
    async def _fetch_tools(self):
        """Fetch available tools from the MCP server"""
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        await self._send_request(tools_request)
        response = await self._receive_response()
        
        if "error" in response:
            raise Exception(f"Failed to fetch tools: {response['error']}")
        
        self.tools = []
        for tool_info in response.get("result", {}).get("tools", []):
            tool = MCPTool(
                name=tool_info["name"],
                description=tool_info["description"],
                parameters=tool_info.get("inputSchema", {})
            )
            self.tools.append(tool)
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool on the MCP server"""
        tool_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        await self._send_request(tool_request)
        response = await self._receive_response()
        
        if "error" in response:
            return f"Tool call failed: {response['error']}"
        
        result = response.get("result", {})
        if "content" in result:
            content = result["content"]
            if isinstance(content, list) and len(content) > 0:
                return content[0].get("text", str(content))
            return str(content)
        
        return str(result)
    
    async def stop(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            await self.process.wait()


class ReActAgent:
    def __init__(self, llm: LLMInterface, mcp_client: MCPClient, max_iterations: int = 10):
        self.llm = llm
        self.mcp_client = mcp_client
        self.max_iterations = max_iterations
        self.logger = logging.getLogger(__name__)
        self.conversation_history: List[ReActStep] = []
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt with available tools"""
        tools_desc = "\n".join([
            f"- {tool.name}: {tool.description}"
            for tool in self.mcp_client.tools
        ])
        
        return f"""You are a ReAct (Reasoning and Acting) agent. You can reason about problems and take actions to solve them.

Available tools:
{tools_desc}

You should follow this format:
Thought: [your reasoning about what to do next]
Action: [the action to take, should be one of the available tools]
Action Input: [the input to the action as a JSON object]
Observation: [you will see the result of the action here]

You can continue this Thought/Action/Action Input/Observation cycle until you have enough information to provide a final answer.

When you have enough information, provide your final answer starting with "Final Answer:".

Remember:
1. Always think step by step
2. Use tools when you need information or want to perform actions
3. Be specific about what information you need
4. Provide a clear final answer when you're done
"""
    
    def _parse_llm_response(self, response: str) -> ReActStep:
        """Parse the LLM response into a ReAct step"""
        thought_match = re.search(r"Thought:\s*(.*?)(?=\nAction:|$)", response, re.DOTALL)
        action_match = re.search(r"Action:\s*(.*?)(?=\nAction Input:|$)", response, re.DOTALL)
        action_input_match = re.search(r"Action Input:\s*(.*?)(?=\nObservation:|$)", response, re.DOTALL)
        
        thought = thought_match.group(1).strip() if thought_match else ""
        action = action_match.group(1).strip() if action_match else None
        
        action_input = None
        if action_input_match:
            try:
                action_input = json.loads(action_input_match.group(1).strip())
            except json.JSONDecodeError:
                action_input = {"query": action_input_match.group(1).strip()}
        
        return ReActStep(thought=thought, action=action, action_input=action_input)
    
    async def run(self, query: str) -> str:
        """Run the ReAct agent to answer a query"""
        self.conversation_history = []
        
        messages = [
            SystemMessage(content=self._create_system_prompt()),
            HumanMessage(content=f"Human: {query}")
        ]
        
        for iteration in range(self.max_iterations):
            self.logger.info(f"ReAct iteration {iteration + 1}")
            
            # Get LLM response
            llm_response = await self.llm.chat(messages)
            
            # Check for final answer
            if "Final Answer:" in llm_response:
                final_answer = llm_response.split("Final Answer:")[1].strip()
                self.logger.info("ReAct agent completed successfully")
                return final_answer
            
            # Parse the response
            step = self._parse_llm_response(llm_response)
            
            if not step.action:
                step.observation = "No action specified. Please specify an action to take."
            else:
                # Execute the action
                if step.action in [tool.name for tool in self.mcp_client.tools]:
                    try:
                        step.observation = await self.mcp_client.call_tool(
                            step.action, 
                            step.action_input or {}
                        )
                    except Exception as e:
                        step.observation = f"Error executing tool {step.action}: {str(e)}"
                else:
                    step.observation = f"Unknown tool: {step.action}. Available tools: {[tool.name for tool in self.mcp_client.tools]}"
            
            self.conversation_history.append(step)
            
            # Add the step to conversation
            messages.append(AIMessage(content=llm_response))
            messages.append(HumanMessage(content=f"Observation: {step.observation}"))
        
        return "Maximum iterations reached without finding a final answer."


class LLMFactory:
    @staticmethod
    def create_llm(provider: LLMProvider, **kwargs) -> LLMInterface:
        """Factory method to create LLM instances"""
        if provider == LLMProvider.OPENAI:
            return OpenAILLM(**kwargs)
        elif provider == LLMProvider.ANTHROPIC:
            return AnthropicLLM(**kwargs)
        elif provider == LLMProvider.GOOGLE:
            return GoogleLLM(**kwargs)
        elif provider == LLMProvider.GROQ:
            return GroqLLM(**kwargs)
        elif provider == LLMProvider.OPENROUTER:
            return OpenRouterLLM(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")


async def main():
    """Example usage of the ReAct Agent"""
    logging.basicConfig(level=logging.INFO)
    
    # Configure your LLM
    llm = LLMFactory.create_llm(
        LLMProvider.OPENAI,
        model="gpt-4",
        api_key="your-openai-api-key"  # Set your API key
    )
    
    # Configure your MCP server command
    mcp_server_command = ["python", "-m", "mcp_server"]  # Replace with your MCP server command
    
    # Create MCP client
    mcp_client = MCPClient(mcp_server_command)
    
    try:
        # Start MCP client
        await mcp_client.start()
        
        # Create ReAct agent
        agent = ReActAgent(llm, mcp_client)
        
        # Run the agent
        query = "What is the current weather in New York?"
        result = await agent.run(query)
        
        print(f"Query: {query}")
        print(f"Answer: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        await mcp_client.stop()


if __name__ == "__main__":
    asyncio.run(main())