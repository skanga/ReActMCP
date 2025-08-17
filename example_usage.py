import asyncio
import logging
import os
import sys
from react_agent import ReActAgent, MCPClient, LLMFactory
from config import ConfigLoader, LLMProvider, MCPServerConfig

async def example_with_hello_mcp():
    """Example using our local hello MCP server"""
    logging.basicConfig(level=logging.INFO)
    
    # Load configuration from environment
    try:
        config = ConfigLoader.load_from_env()
        print(f"Using {config.llm.provider.value} with model: {config.llm.model}")
        
        # Create LLM from config
        llm_kwargs = {
            "model": config.llm.model,
            "api_key": config.llm.api_key
        }
        
        # Add provider-specific parameters
        if config.llm.base_url:
            llm_kwargs["base_url"] = config.llm.base_url
        
        llm = LLMFactory.create_llm(config.llm.provider, **llm_kwargs)
        
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {e}")
        print("\nQuick Fix:")
        print("   1. Run: python test_config.py  (to check your configuration)")
        print("   2. Copy: copy .env.example .env")
        print("   3. Edit .env with your API key")
        return
    
    # Our hello MCP server command
    mcp_server_command = [sys.executable, "hello_mcp_server.py"]
    
    mcp_client = MCPClient(mcp_server_command)
    
    try:
        await mcp_client.start()
        agent = ReActAgent(llm, mcp_client, max_iterations=config.max_iterations)
        
        print(f"Available tools: {[tool.name for tool in mcp_client.tools]}")
        
        # Example queries
        queries = [
            "Say hello to Alice with a warm greeting",
            "What time is it right now?",
            "Calculate 25 + 17 * 3",
            "Echo the message 'Hello from ReAct agent!'"
        ]
        
        for query in queries:
            print(f"\n{'='*50}")
            print(f"Query: {query}")
            print(f"{'='*50}")
            
            result = await agent.run(query)
            print(f"Answer: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await mcp_client.stop()


async def example_with_data_analyst_mcp():
    """Example using our data analyst MCP server"""
    logging.basicConfig(level=logging.INFO)
    
    # Load configuration from environment
    try:
        config = ConfigLoader.load_from_env()
        print(f"Using {config.llm.provider.value} with model: {config.llm.model}")
        
        # Create LLM from config
        llm_kwargs = {
            "model": config.llm.model,
            "api_key": config.llm.api_key
        }
        
        # Add provider-specific parameters
        if config.llm.base_url:
            llm_kwargs["base_url"] = config.llm.base_url
        
        llm = LLMFactory.create_llm(config.llm.provider, **llm_kwargs)
        
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {e}")
        print("\nQuick Fix:")
        print("   1. Run: python test_config.py  (to check your configuration)")
        print("   2. Copy: copy .env.example .env")
        print("   3. Edit .env with your API key")
        return
    
    # Our data analyst MCP server command
    mcp_server_command = [sys.executable, "data_analyst_mcp_server.py"]
    
    mcp_client = MCPClient(mcp_server_command)
    
    try:
        await mcp_client.start()
        agent = ReActAgent(llm, mcp_client, max_iterations=config.max_iterations)
        
        print(f"Available tools: {[tool.name for tool in mcp_client.tools]}")
        
        # Example business analysis query
        query = """Create a sales dataset with 50 records, analyze it for summary statistics, 
        filter for high-value sales above $2000, and provide business insights about the performance patterns."""
        
        print(f"\n{'='*60}")
        print(f"Business Analysis Query: {query}")
        print(f"{'='*60}")
        
        result = await agent.run(query)
        print(f"\nBusiness Analysis Result: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await mcp_client.stop()


async def example_with_filesystem_mcp():
    """Example using a filesystem MCP server"""
    logging.basicConfig(level=logging.INFO)
    
    # Load configuration from environment
    try:
        config = ConfigLoader.load_from_env()
        print(f"Using {config.llm.provider.value} with model: {config.llm.model}")
        
        # Create LLM from config
        llm_kwargs = {
            "model": config.llm.model,
            "api_key": config.llm.api_key
        }
        
        # Add provider-specific parameters
        if config.llm.base_url:
            llm_kwargs["base_url"] = config.llm.base_url
        
        llm = LLMFactory.create_llm(config.llm.provider, **llm_kwargs)
        
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {e}")
        print("Please configure your .env file with LLM settings")
        return
    
    # Example MCP server command (replace with actual MCP server)
    mcp_server_command = [
        "npx", "@modelcontextprotocol/server-filesystem", 
        "/path/to/allowed/directory"
    ]
    
    mcp_client = MCPClient(mcp_server_command)
    
    try:
        await mcp_client.start()
        agent = ReActAgent(llm, mcp_client)
        
        # Example queries
        queries = [
            "What files are in the current directory?",
            "Read the contents of README.md if it exists",
            "Create a new file called 'test.txt' with some example content"
        ]
        
        for query in queries:
            print(f"\n{'='*50}")
            print(f"Query: {query}")
            print(f"{'='*50}")
            
            result = await agent.run(query)
            print(f"Answer: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await mcp_client.stop()


async def example_with_web_search_mcp():
    """Example using a web search MCP server"""
    logging.basicConfig(level=logging.INFO)
    
    # Load configuration from environment
    try:
        config = ConfigLoader.load_from_env()
        print(f"Using {config.llm.provider.value} with model: {config.llm.model}")
        
        # Create LLM from config
        llm_kwargs = {
            "model": config.llm.model,
            "api_key": config.llm.api_key
        }
        
        # Add provider-specific parameters
        if config.llm.base_url:
            llm_kwargs["base_url"] = config.llm.base_url
        
        llm = LLMFactory.create_llm(config.llm.provider, **llm_kwargs)
        
    except Exception as e:
        print(f"ERROR: Failed to load configuration: {e}")
        print("Please configure your .env file with LLM settings")
        return
    
    # Example web search MCP server command
    mcp_server_command = [
        "npx", "@modelcontextprotocol/server-brave-search"
    ]
    
    mcp_client = MCPClient(mcp_server_command)
    
    try:
        await mcp_client.start()
        agent = ReActAgent(llm, mcp_client, max_iterations=config.max_iterations)
        
        query = "What is the current weather in San Francisco and what are the top news stories today?"
        
        print(f"Query: {query}")
        result = await agent.run(query)
        print(f"Answer: {result}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await mcp_client.stop()


async def example_with_config():
    """Example using configuration file"""
    logging.basicConfig(level=logging.INFO)
    
    # Set up environment variables for this example
    os.environ.update({
        "LLM_PROVIDER": "openai",
        "LLM_MODEL": "gpt-4",
        "LLM_API_KEY": "your-openai-api-key",
        "MCP_SERVER_COUNT": "1",
        "MCP_SERVER_0_NAME": "filesystem",
        "MCP_SERVER_0_COMMAND": "npx @modelcontextprotocol/server-filesystem /tmp",
        "MCP_SERVER_0_DESCRIPTION": "Filesystem access server"
    })
    
    # Load configuration
    config = ConfigLoader.load_from_env()
    
    # Create LLM
    llm = LLMFactory.create_llm(
        config.llm.provider,
        model=config.llm.model,
        api_key=config.llm.api_key,
        base_url=config.llm.base_url
    )
    
    # Create and start MCP clients
    mcp_clients = []
    for server_config in config.mcp_servers:
        client = MCPClient(server_config.command)
        await client.start()
        mcp_clients.append(client)
    
    try:
        # Use the first MCP client for this example
        if mcp_clients:
            agent = ReActAgent(llm, mcp_clients[0], max_iterations=config.max_iterations)
            
            query = "List the available tools and their descriptions"
            result = await agent.run(query)
            print(f"Query: {query}")
            print(f"Answer: {result}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up all MCP clients
        for client in mcp_clients:
            await client.stop()


async def multi_provider_example():
    """Example showing different LLM providers"""
    logging.basicConfig(level=logging.INFO)
    
    # Example MCP server
    mcp_server_command = ["echo", "{}"]  # Dummy command for testing
    mcp_client = MCPClient(mcp_server_command)
    
    providers = [
        (LLMProvider.OPENAI, {"model": "gpt-3.5-turbo", "api_key": "your-key"}),
        (LLMProvider.ANTHROPIC, {"model": "claude-3-haiku-20240307", "api_key": "your-key"}),
        (LLMProvider.GOOGLE, {"model": "gemini-pro", "api_key": "your-key"}),
        (LLMProvider.GROQ, {"model": "llama2-70b-4096", "api_key": "your-key"}),
    ]
    
    query = "Hello, what can you help me with?"
    
    for provider, kwargs in providers:
        try:
            print(f"\n--- Testing {provider.value} ---")
            llm = LLMFactory.create_llm(provider, **kwargs)
            
            # For this example, we'll just test the LLM directly
            from langchain.schema import HumanMessage
            response = await llm.chat([HumanMessage(content=query)])
            print(f"Response: {response}")
            
        except Exception as e:
            print(f"Error with {provider.value}: {e}")


async def interactive_mode():
    """Interactive mode for testing the agent"""
    logging.basicConfig(level=logging.INFO)
    
    print("ReAct Agent Interactive Mode")
    print("=" * 40)
    
    # Configure LLM
    provider = input("Choose LLM provider (openai/anthropic/google/groq): ").strip().lower()
    if provider not in ["openai", "anthropic", "google", "groq"]:
        provider = "openai"
    
    api_key = input(f"Enter your {provider} API key: ").strip()
    
    llm = LLMFactory.create_llm(
        LLMProvider(provider),
        api_key=api_key
    )
    
    # Configure MCP server
    mcp_command = input("Enter MCP server command (space-separated): ").strip().split()
    if not mcp_command:
        print("No MCP server specified, using dummy server")
        mcp_command = ["echo", "{}"]
    
    mcp_client = MCPClient(mcp_command)
    
    try:
        await mcp_client.start()
        agent = ReActAgent(llm, mcp_client)
        
        print(f"\nAvailable tools: {[tool.name for tool in mcp_client.tools]}")
        print("\nEnter your queries (type 'quit' to exit):")
        
        while True:
            query = input("\n> ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if query:
                try:
                    result = await agent.run(query)
                    print(f"\nAnswer: {result}")
                except Exception as e:
                    print(f"Error: {e}")
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await mcp_client.stop()


if __name__ == "__main__":
    print("ReAct Agent Examples")
    print("1. Hello MCP server example (local)")
    print("2. Data Analyst MCP server example (business intelligence)")
    print("3. Filesystem MCP example")
    print("4. Web search MCP example") 
    print("5. Configuration-based example")
    print("6. Multi-provider test")
    print("7. Interactive mode")
    
    choice = input("Choose an example (1-7): ").strip()
    
    if choice == "1":
        asyncio.run(example_with_hello_mcp())
    elif choice == "2":
        asyncio.run(example_with_data_analyst_mcp())
    elif choice == "3":
        asyncio.run(example_with_filesystem_mcp())
    elif choice == "4":
        asyncio.run(example_with_web_search_mcp())
    elif choice == "5":
        asyncio.run(example_with_config())
    elif choice == "6":
        asyncio.run(multi_provider_example())
    elif choice == "7":
        asyncio.run(interactive_mode())
    else:
        print("Invalid choice, running hello MCP example")
        asyncio.run(example_with_hello_mcp())
