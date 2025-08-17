# ReAct AI Agent with MCP Client

A powerful Python implementation of a ReAct (Reasoning and Acting) AI agent that can communicate with MCP (Model Context Protocol) servers and use various LLM providers. Features comprehensive business intelligence tools and multiple demonstration scenarios.

## 🚀 Features

- **🧠 ReAct Architecture**: Implements the Reasoning and Acting pattern for intelligent problem-solving
- **🔗 MCP Client**: Full STDIO protocol support for MCP servers
- **🤖 Multi-LLM Support**: OpenAI, Anthropic, Google, Groq, OpenRouter
- **📊 Data Analysis**: Advanced data analyst MCP server with business intelligence tools
- **⚡ Async Operations**: Fully asynchronous for optimal performance
- **⚙️ Environment Configuration**: Easy setup with .env file support
- **🎯 Multiple Demos**: 5+ different showcase scenarios

## 📁 Project Structure

```
PyMCP/
├── 📋 Core Components
│   ├── react_agent.py              # Main ReAct agent implementation
│   ├── config.py                   # Configuration management (.env support)
│   └── requirements.txt             # Dependencies
│
├── 🖥️ MCP Servers
│   ├── hello_mcp_server.py         # Simple greeting/utility server
│   └── data_analyst_mcp_server.py  # Advanced business intelligence server
│
├── 🎮 Examples & Demos
│   ├── example_usage.py            # 7 different example scenarios
│   ├── power_demo.py               # Ultimate business analysis challenge
│   └── showcase_demo.py            # 6 comprehensive demonstrations
│
├── 🔧 Utilities
│   └── test_config.py              # Configuration testing
│
└── 📚 Documentation
    ├── README.md                   # This file
    ├── SETUP.md                    # Quick start guide
    └── .env.example                # Configuration template
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Your LLM
```bash
copy .env.example .env
# Edit .env with your API key and preferred provider
```

### 3. Test Configuration
```bash
python test_config.py
```

### 4. Run Examples
```bash
# Quick start with multiple options
python example_usage.py

# Ultimate business analysis demo
python power_demo.py

# Comprehensive showcase (6 demos)
python showcase_demo.py
```

## ⚙️ Configuration

Configure your preferred LLM provider in `.env`:

### OpenAI
```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your-openai-api-key
```

### Groq (Free Tier Available!)
```env
LLM_PROVIDER=groq
LLM_MODEL=meta-llama/llama-3-8b-8192
LLM_API_KEY=your-groq-api-key
```

### Anthropic
```env
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
LLM_API_KEY=your-anthropic-api-key
```

### Google
```env
LLM_PROVIDER=google
LLM_MODEL=gemini-pro
LLM_API_KEY=your-google-api-key
```

### OpenRouter
```env
LLM_PROVIDER=openrouter
LLM_MODEL=anthropic/claude-3-sonnet
LLM_API_KEY=your-openrouter-api-key
```

## 🎯 Demos & Examples

### 1. `example_usage.py` - Interactive Examples (7 Options)
Choose from multiple scenarios:
1. **Hello MCP Server** - Simple greeting and utility tools
2. **Data Analyst MCP** - Business intelligence and data analysis
3. **Filesystem MCP** - File system operations (requires NPX)
4. **Web Search MCP** - Web search capabilities (requires NPX)
5. **Configuration Demo** - Environment-based setup
6. **Multi-Provider Test** - Test different LLM providers
7. **Interactive Mode** - Ask your own questions

```bash
python example_usage.py
# Choose option 1 or 2 for local servers (no NPX required)
```

### 2. `power_demo.py` - Ultimate Business Challenge
The most comprehensive demonstration featuring:
- **Complex Problem**: Multi-step business analysis
- **200 Record Dataset**: Realistic sales data
- **8 Analysis Steps**: From data creation to executive recommendations
- **Executive Report**: Professional business insights

```bash
python power_demo.py
# Choose option 1 for full power demo
```

### 3. `showcase_demo.py` - Comprehensive Showcase (6 Demos)
Professional demonstration suite:
1. **Business Data Analysis** - Complex reasoning with sales data
2. **Data Detective** - Pattern finding across multiple datasets
3. **Predictive Analytics** - Forecasting and trend analysis
4. **Multi-step Optimization** - 5-step business optimization
5. **Comparative Analysis** - Multiple dataset comparison
6. **Interactive Mode** - Custom queries

```bash
python showcase_demo.py
# Choose individual demos or run all sequentially
```

## 🛠️ MCP Servers

### Hello MCP Server (`hello_mcp_server.py`)
Simple server with basic utilities:
- **say_hello** - Greeting with custom messages
- **get_time** - Current time in multiple formats
- **echo** - Message echoing
- **calculate** - Basic arithmetic

### Data Analyst MCP Server (`data_analyst_mcp_server.py`)
Advanced business intelligence server:
- **create_dataset** - Generate realistic business data (sales, weather, students)
- **analyze_data** - Statistical analysis (summary, correlation, trends, outliers)
- **filter_data** - Complex data filtering with conditions
- **visualize_data** - Text-based charts and histograms
- **predict_trend** - Trend forecasting and predictions
- **save_to_file/load_from_file** - Data persistence

## 🎯 ReAct Agent Capabilities

### Intelligent Reasoning Chain
```
Thought: "I need to analyze business performance"
Action: create_dataset
Observation: "Created sales dataset with 200 records"

Thought: "Now I should understand the current situation"  
Action: analyze_data
Observation: "Average sales: $2,345, range: $100-$5,000"

Thought: "I need to identify top performers"
Action: filter_data
Observation: "Found 45 high-value transactions"
...
```

### Advanced Problem Solving
- **Multi-step Planning** - Breaks complex requests into manageable steps
- **Tool Orchestration** - Intelligently chains tools together
- **Adaptive Reasoning** - Adjusts approach based on observations
- **Goal Persistence** - Stays focused on end objective

## 🔑 Getting API Keys

### Groq (Recommended - Free Tier)
1. Go to https://console.groq.com/keys
2. Sign up for free account
3. Generate API key (generous free tier)

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create account and API key
3. Add billing information

### Anthropic
1. Go to https://console.anthropic.com/
2. Create account and get API key

## 🎮 Example Usage Scenarios

### Business Analysis
```python
# The agent will:
# 1. Create a comprehensive sales dataset
# 2. Perform statistical analysis
# 3. Filter for high-performing products
# 4. Identify outliers and problems
# 5. Analyze trends and patterns
# 6. Create visualizations
# 7. Make predictions
# 8. Provide executive recommendations
```

### Data Detective Work
```python
# The agent will:
# 1. Create multiple datasets
# 2. Investigate patterns and correlations
# 3. Find anomalies and outliers
# 4. Cross-reference different data sources
# 5. Provide insights and conclusions
```

### Interactive Problem Solving
```python
# Ask complex questions like:
# - "Create a dataset, analyze trends, and predict future performance"
# - "Compare different data patterns and find correlations"  
# - "Investigate outliers and provide business recommendations"
```

## 🏗️ How It Works

### ReAct Pattern Implementation
1. **Reason** - Agent thinks about what to do next
2. **Act** - Calls appropriate MCP tools
3. **Observe** - Analyzes results and adjusts approach
4. **Repeat** - Continues until goal is achieved

### MCP Integration
- **STDIO Communication** - Full JSON-RPC protocol support
- **Tool Discovery** - Automatic detection of available tools
- **Error Handling** - Robust error recovery and reporting
- **Async Operations** - Non-blocking tool execution

## 🐛 Troubleshooting

**Configuration Issues**
```bash
python test_config.py  # Test your .env setup
```

**Missing Dependencies**
```bash
pip install -r requirements.txt
```

**API Key Problems**
- Verify key is valid and has credits
- Check provider is correctly set in .env
- Try the free Groq option for testing

## 🔧 Development

### Adding New LLM Providers
1. Create new LLM class implementing `LLMInterface`
2. Add to `LLMProvider` enum
3. Update `LLMFactory.create_llm()`

### Adding New MCP Servers
1. Follow MCP protocol specification
2. Implement tool discovery and execution
3. Add to example configurations

### Creating Custom Demos
1. Use `ConfigLoader.load_from_env()` for setup
2. Create `MCPClient` with your server
3. Initialize `ReActAgent` with your LLM

## 📄 License

This project is open source. Feel free to use, modify, and extend as needed.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional LLM providers
- New MCP server implementations
- Enhanced ReAct strategies
- More demonstration scenarios
- Performance optimizations