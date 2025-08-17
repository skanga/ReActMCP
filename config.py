import os
from dataclasses import dataclass
from typing import Optional, List
from react_agent import LLMProvider

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

@dataclass
class LLMConfig:
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None

@dataclass
class MCPServerConfig:
    name: str
    command: List[str]
    description: str = ""

@dataclass
class AgentConfig:
    llm: LLMConfig
    mcp_servers: List[MCPServerConfig]
    max_iterations: int = 10
    log_level: str = "INFO"

class ConfigLoader:
    @staticmethod
    def load_from_env() -> AgentConfig:
        """Load configuration from .env file and environment variables"""
        
        # Load .env file if available
        if DOTENV_AVAILABLE:
            env_file = load_dotenv()  # This loads .env file into environment variables
            if env_file:
                print("Loaded configuration from .env file")
            else:
                print("No .env file found, using environment variables only")
        else:
            print("python-dotenv not installed, using environment variables only")
        
        # LLM Configuration
        provider_str = os.getenv("LLM_PROVIDER", "openai").lower()
        provider = LLMProvider(provider_str)
        
        llm_config = LLMConfig(
            provider=provider,
            model=os.getenv("LLM_MODEL", ConfigLoader._get_default_model(provider)),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )
        
        # Validate configuration
        if not llm_config.api_key:
            raise ValueError(f"Missing API key for {provider.value}. Please set LLM_API_KEY in your .env file.")
        
        # MCP Server Configuration
        mcp_servers = []
        
        # Check for MCP server configurations
        server_count = int(os.getenv("MCP_SERVER_COUNT", "0"))
        for i in range(server_count):
            name = os.getenv(f"MCP_SERVER_{i}_NAME", f"server_{i}")
            command = os.getenv(f"MCP_SERVER_{i}_COMMAND", "").split()
            description = os.getenv(f"MCP_SERVER_{i}_DESCRIPTION", "")
            
            if command:
                mcp_servers.append(MCPServerConfig(
                    name=name,
                    command=command,
                    description=description
                ))
        
        return AgentConfig(
            llm=llm_config,
            mcp_servers=mcp_servers,
            max_iterations=int(os.getenv("MAX_ITERATIONS", "10")),
            log_level=os.getenv("LOG_LEVEL", "INFO")
        )
    
    @staticmethod
    def _get_default_model(provider: LLMProvider) -> str:
        """Get default model for each provider"""
        defaults = {
            LLMProvider.OPENAI: "gpt-4",
            LLMProvider.ANTHROPIC: "claude-3-sonnet-20240229",
            LLMProvider.GOOGLE: "gemini-pro",
            LLMProvider.GROQ: "openai/gpt-oss-120b",
            LLMProvider.OPENROUTER: "anthropic/claude-3-sonnet"
        }
        return defaults.get(provider, "gpt-4")


# Example configurations for different providers
EXAMPLE_CONFIGS = {
    "openai": {
        "LLM_PROVIDER": "openai",
        "LLM_MODEL": "gpt-4",
        "LLM_API_KEY": "your-openai-api-key"
    },
    "anthropic": {
        "LLM_PROVIDER": "anthropic",
        "LLM_MODEL": "claude-3-sonnet-20240229",
        "LLM_API_KEY": "your-anthropic-api-key"
    },
    "google": {
        "LLM_PROVIDER": "google",
        "LLM_MODEL": "gemini-pro",
        "LLM_API_KEY": "your-google-api-key"
    },
    "groq": {
        "LLM_PROVIDER": "groq",
        "LLM_MODEL": "mixtral-8x7b-32768",
        "LLM_API_KEY": "your-groq-api-key"
    },
    "bedrock": {
        "LLM_PROVIDER": "bedrock",
        "LLM_MODEL": "anthropic.claude-3-sonnet-20240229-v1:0",
        "AWS_REGION": "us-east-1"
    },
    "azure": {
        "LLM_PROVIDER": "azure",
        "LLM_MODEL": "gpt-4",
        "LLM_API_KEY": "your-azure-api-key",
        "AZURE_DEPLOYMENT_NAME": "your-deployment-name",
        "AZURE_ENDPOINT": "https://your-resource.openai.azure.com/"
    },
    "openrouter": {
        "LLM_PROVIDER": "openrouter",
        "LLM_MODEL": "anthropic/claude-3-sonnet",
        "LLM_API_KEY": "your-openrouter-api-key"
    }
}