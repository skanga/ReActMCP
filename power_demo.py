#!/usr/bin/env python3
"""
POWER DEMO: The Ultimate ReAct Agent Showcase
Demonstrates complex multi-step reasoning with real business scenarios
"""

import sys
import asyncio
import logging
from react_agent import ReActAgent, MCPClient, LLMFactory
from config import ConfigLoader

async def run_power_demo():
    """Run the ultimate power demonstration"""
    
    print("""
REACT AGENT POWER DEMONSTRATION
==================================

This demo will showcase the agent's ability to:
* Reason through complex business problems
* Chain multiple tools intelligently  
* Perform deep data analysis
* Provide actionable recommendations
* Think step-by-step like a human analyst

""")
    
    # Setup
    logging.basicConfig(level=logging.WARNING)  # Reduce noise
    
    # Load configuration from environment
    try:
        config = ConfigLoader.load_from_env()
        print(f" Using {config.llm.provider.value} with model: {config.llm.model}")
        
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
        print(f"Failed to load configuration: {e}")
        print("\nQuick Fix:")
        print("   1. Run: python test_config.py  (to check your configuration)")
        print("   2. Copy: copy .env.example .env")
        print("   3. Edit .env with your API key")
        print("   4. Try again!")
        return
    
    mcp_client = MCPClient([sys.executable, "data_analyst_mcp_server.py"])
    
    try:
        await mcp_client.start()
        agent = ReActAgent(llm, mcp_client, max_iterations=config.max_iterations)
        
        print(f" Available tools: {[tool.name for tool in mcp_client.tools]}\n")
        
        # THE ULTIMATE CHALLENGE
        challenge = """
        You are a senior business analyst. I need you to solve this complex business problem:
        
        Our company needs to optimize product performance. Please:
        
        1. Create a comprehensive sales dataset (200 records) to simulate our business
        2. Perform a complete analysis to understand our current situation
        3. Identify our top-performing products by filtering high-value sales
        4. Investigate any concerning outliers that might indicate problems
        5. Analyze trends to understand market direction
        6. Create a visualization to present key findings
        7. Make specific predictions for the next quarter
        8. Provide 3 concrete recommendations for improving overall performance
        
        This analysis will be presented to the executive team, so please be thorough 
        and professional in your approach.
        """
        
        print("THE CHALLENGE:")
        print("=" * 50)
        print(challenge)
        print("=" * 50)
        
        print("\nAGENT THINKING AND WORKING:")
        print("-" * 50)
        
        # Run the challenge
        result = await agent.run(challenge)
        
        print("\n" + "=" * 60)
        print("FINAL REPORT:")
        print("=" * 60)
        print(result)
        print("=" * 60)
        
        print("""
DEMO COMPLETE!

The ReAct agent just demonstrated:
* Complex multi-step reasoning (8 different tasks)
* Intelligent tool selection and chaining
* Data creation, analysis, and visualization
* Business insight generation
* Predictive analytics
* Strategic recommendations

This level of autonomous problem-solving showcases the true power 
of ReAct agents in real-world business scenarios!
""")

    except Exception as e:
        print(f"Demo failed: {e}")
        print("\nTroubleshooting:")
        print("   - Check your API key is valid and has sufficient credits")
        print("   - Verify your .env file contains correct LLM configuration")
        print("   - Try with a different model or provider")
        
    finally:
        await mcp_client.stop()


async def run_quick_demo():
    """Quick demo with simpler setup"""
    print("QUICK REACT DEMO (No API key required)")
    print("=" * 40)
    
    # This demo shows the structure even without a real LLM
    mcp_client = MCPClient([sys.executable, "data_analyst_mcp_server.py"])
    
    try:
        await mcp_client.start()
        print(f"MCP Server started successfully!")
        print(f"Available tools: {[tool.name for tool in mcp_client.tools]}")
        
        print("""
Here's what the ReAct agent would do with these tools:

REASONING PROCESS:
1. "I need to analyze business data for insights"
2. "First, I should create a dataset using create_dataset"
3. "Then analyze it with analyze_data for summary stats"
4. "I should filter for high-value transactions"
5. "Check for outliers that might indicate problems"
6. "Analyze trends to understand direction"
7. "Make predictions for future planning"
8. "Provide actionable recommendations"

TOOL CHAIN:
create_dataset → analyze_data → filter_data → analyze_data 
→ visualize_data → predict_trend → [final reasoning]

This demonstrates the ReAct pattern:
• REASON about what to do next
• ACT by calling appropriate tools  
• OBSERVE results and adjust approach
• REPEAT until goal is achieved

With a real LLM, you'd see this happening step by step!
        """)
        
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        await mcp_client.stop()


async def main():
    print("Choose demo mode:")
    print("1. Full Power Demo (requires LLM API key in .env file)")
    print("2. Quick Demo (shows structure without LLM)")
    print("\nFor option 1: Copy .env.example to .env and configure your API key")
    
    choice = input("\nSelect (1 or 2): ").strip()
    
    if choice == "1":
        await run_power_demo()
    else:
        await run_quick_demo()


if __name__ == "__main__":
    asyncio.run(main())