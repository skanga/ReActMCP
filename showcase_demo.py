#!/usr/bin/env python3
"""
Showcase Demo: Demonstrating the power of ReAct Agent
This script provides compelling examples that showcase the ReAct agent's reasoning abilities
"""

import sys
import asyncio
import logging
from config import ConfigLoader
from react_agent import ReActAgent, MCPClient, LLMFactory

class ShowcaseDemo:
    def __init__(self):
        self.llm = None
        self.mcp_client = None
        self.agent = None
        
    async def setup(self):
        """Setup the demo environment"""
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
            
            self.llm = LLMFactory.create_llm(config.llm.provider, **llm_kwargs)
            self.max_iterations = config.max_iterations
            
        except Exception as e:
            print(f"ERROR: Failed to load configuration: {e}")
            print("\nQuick Fix:")
            print("   1. Run: python test_config.py  (to check your configuration)")
            print("   2. Copy: copy .env.example .env")
            print("   3. Edit .env with your API key")
            raise
        
        # Create MCP client with advanced server
        self.mcp_client = MCPClient([sys.executable, "data_analyst_mcp_server.py"])
        await self.mcp_client.start()
        
        # Create ReAct agent with configured iterations
        self.agent = ReActAgent(self.llm, self.mcp_client, max_iterations=self.max_iterations)
        
        print("ReAct Agent Showcase Demo")
        print("=" * 50)
        print(f"Available tools: {[tool.name for tool in self.mcp_client.tools]}")
        print("=" * 50)
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.mcp_client:
            await self.mcp_client.stop()
    
    async def demo_business_analysis(self):
        """Demo 1: Complex Business Data Analysis"""
        print("\nDEMO 1: BUSINESS DATA ANALYSIS")
        print("=" * 40)
        
        query = """I need to analyze sales performance and make business recommendations. 
        Please create a sales dataset, analyze it for trends and outliers, filter for high-performing products, 
        and provide actionable insights with predictions for the next quarter."""
        
        print(f"Challenge: {query}")
        print("\nReAct Agent thinking and working...")
        print("-" * 40)
        
        result = await self.agent.run(query)
        
        print(f"\nFinal Analysis: {result}")
        print("=" * 40)
    
    async def demo_data_detective(self):
        """Demo 2: Data Detective - Finding Patterns"""
        print("\nDEMO 2: DATA DETECTIVE")
        print("=" * 40)
        
        query = """Act as a data detective. Create a weather dataset and a student performance dataset. 
        Then analyze both to find any interesting patterns, correlations, or anomalies. 
        Create visualizations and provide insights about what the data reveals."""
        
        print(f"Challenge: {query}")
        print("\nReAct Agent investigating...")
        print("-" * 40)
        
        result = await self.agent.run(query)
        
        print(f"\nDetective Report: {result}")
        print("=" * 40)
    
    async def demo_predictive_insights(self):
        """Demo 3: Predictive Analytics"""
        print("\nDEMO 3: PREDICTIVE ANALYTICS")
        print("=" * 40)
        
        query = """I want to understand future trends. Create a sales dataset, analyze the trends, 
        identify the best performing products by filtering the data, and then make predictions 
        for the next 6 periods. Also create a histogram visualization of the sales amounts."""
        
        print(f"Challenge: {query}")
        print("\nReAct Agent forecasting...")
        print("-" * 40)
        
        result = await self.agent.run(query)
        
        print(f"\nPredictive Insights: {result}")
        print("=" * 40)
    
    async def demo_multi_step_optimization(self):
        """Demo 4: Multi-step Optimization Problem"""
        print("\nDEMO 4: OPTIMIZATION CHALLENGE")
        print("=" * 40)
        
        query = """Help me optimize our business operations. Create a sales dataset, then:
        1. Find the top-performing products (filter sales > 2000)
        2. Analyze correlations between sales amount, quantity, and customer ratings
        3. Identify any outliers that might indicate problems
        4. Make trend predictions for the high-performing products
        5. Provide specific recommendations for improving overall performance"""
        
        print(f"Challenge: {query}")
        print("\nReAct Agent optimizing...")
        print("-" * 40)
        
        result = await self.agent.run(query)
        
        print(f"\nOptimization Strategy: {result}")
        print("=" * 40)
    
    async def demo_comparative_analysis(self):
        """Demo 5: Comparative Analysis"""
        print("\nDEMO 5: COMPARATIVE ANALYSIS")
        print("=" * 40)
        
        query = """Perform a comprehensive comparative analysis:
        1. Create both weather and sales datasets (100 records each)
        2. Analyze trends in both datasets
        3. Filter weather data for high temperature days (>75 degrees)
        4. Filter sales data for high-value transactions (>3000)
        5. Compare the patterns and provide insights about data quality and business implications"""
        
        print(f"Challenge: {query}")
        print("\nReAct Agent comparing...")
        print("-" * 40)
        
        result = await self.agent.run(query)
        
        print(f"\nComparative Insights: {result}")
        print("=" * 40)
    
    async def interactive_demo(self):
        """Interactive demo mode"""
        print("\nINTERACTIVE DEMO MODE")
        print("=" * 40)
        print("Ask the ReAct agent complex questions that require multiple tool uses!")
        print("Examples:")
        print("- 'Create a dataset, analyze it, and predict future trends'")
        print("- 'Compare different data patterns and find correlations'")
        print("- 'Investigate outliers and provide business recommendations'")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            query = input("\nYour challenge: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                break
            
            if query:
                try:
                    print(f"\nReAct Agent working on: {query}")
                    print("-" * 30)
                    result = await self.agent.run(query)
                    print(f"\nSolution: {result}")
                    print("=" * 40)
                except Exception as e:
                    print(f"ERROR: Error: {e}")
    
    async def run_all_demos(self):
        """Run all predefined demos"""
        await self.setup()
        
        try:
            await self.demo_business_analysis()
            
            input("\nPress Enter to continue to next demo...")
            await self.demo_data_detective()
            
            input("\nPress Enter to continue to next demo...")
            await self.demo_predictive_insights()
            
            input("\nPress Enter to continue to next demo...")
            await self.demo_multi_step_optimization()
            
            input("\nPress Enter to continue to next demo...")
            await self.demo_comparative_analysis()
            
            print("\nALL DEMOS COMPLETED!")
            print("=" * 50)
            print("The ReAct agent demonstrated:")
            print("* Multi-step reasoning")
            print("* Tool chaining and orchestration")
            print("* Data analysis and insights")
            print("* Predictive capabilities")
            print("* Complex problem solving")
            print("* Business intelligence")
            
        finally:
            await self.cleanup()
    
    async def run_single_demo(self, demo_number: int):
        """Run a single demo by number"""
        await self.setup()
        
        try:
            if demo_number == 1:
                await self.demo_business_analysis()
            elif demo_number == 2:
                await self.demo_data_detective()
            elif demo_number == 3:
                await self.demo_predictive_insights()
            elif demo_number == 4:
                await self.demo_multi_step_optimization()
            elif demo_number == 5:
                await self.demo_comparative_analysis()
            elif demo_number == 6:
                await self.interactive_demo()
            else:
                print("Invalid demo number")
        finally:
            await self.cleanup()


async def main():
    """Main menu for the showcase demo"""
    demo = ShowcaseDemo()
    
    print("ReAct Agent Power Showcase")
    print("=" * 40)
    print("Choose a demonstration:")
    print("1. Business Data Analysis (Complex reasoning)")
    print("2. Data Detective (Pattern finding)")
    print("3. Predictive Analytics (Forecasting)")
    print("4. Multi-step Optimization (Complex problem solving)")
    print("5. Comparative Analysis (Multiple datasets)")
    print("6. Interactive Mode (Ask your own questions)")
    print("7. Run ALL demos sequentially")
    print("0. Exit")
    
    while True:
        try:
            choice = input("\nSelect demo (0-7): ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "7":
                await demo.run_all_demos()
                break
            elif choice in ["1", "2", "3", "4", "5", "6"]:
                await demo.run_single_demo(int(choice))
                break
            else:
                print("ERROR: Invalid choice. Please select 0-7.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"ERROR: Error: {e}")


if __name__ == "__main__":
    print("""
REACT AGENT SHOWCASE
========================

This demonstration showcases the power of ReAct (Reasoning and Acting) agents:

* INTELLIGENT REASONING: The agent thinks through complex problems step by step
* TOOL ORCHESTRATION: Chains multiple tools together to solve complex tasks  
* DATA ANALYSIS: Performs sophisticated data analysis and insights
* PREDICTIVE POWER: Makes forecasts and predictions based on data patterns
* GOAL-ORIENTED: Stays focused on the end goal while adapting its approach

Watch as the agent breaks down complex requests into manageable steps,
reasons through each decision, and delivers comprehensive solutions!
""")
    
    asyncio.run(main())