# Quick Setup Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Your LLM
Copy the example environment file and add your API key:
```bash
copy .env.example .env
# Edit .env with your preferred text editor
```

**Example .env configuration:**
```env
# For OpenAI
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_API_KEY=your-openai-api-key-here

# For Groq (free tier available)
LLM_PROVIDER=groq
LLM_MODEL=meta-llama/llama-4-scout-17b-16e-instruct
LLM_API_KEY=your-groq-api-key-here

# For Anthropic
LLM_PROVIDER=anthropic
LLM_MODEL=claude-3-sonnet-20240229
LLM_API_KEY=your-anthropic-api-key-here
```

### 3. Test Your Configuration
```bash
# Test if .env is loading correctly
python test_config.py
```

### 4. Run Examples
```bash
# Quick showcase
python power_demo.py

# Interactive examples
python example_usage.py

# Full showcase suite
python showcase_demo.py
```

## 🔑 Getting API Keys

### OpenAI
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add billing information if needed

### Groq (Free Tier Available!)
1. Go to https://console.groq.com/keys
2. Sign up for free account
3. Generate API key (generous free tier)

### Anthropic
1. Go to https://console.anthropic.com/
2. Create account and get API key
3. Add to .env file

## 🎯 What to Try

1. **Start Simple**: `python example_usage.py` → Choose option 1 (Hello MCP)
2. **Business Analysis**: Choose option 2 (Data Analyst MCP)
3. **Full Power Demo**: `python power_demo.py` → Option 1
4. **Interactive Showcase**: `python showcase_demo.py`

## 🐛 Troubleshooting

**"No module named 'langchain'"**
```bash
pip install -r requirements.txt
```

**"Failed to load configuration"**
- Make sure .env file exists
- Check API key is valid
- Verify LLM_PROVIDER is supported

**"Tool execution failed"**
- Check internet connection
- Verify API key has sufficient credits
- Try a different model/provider

## 💡 Pro Tips

- **Free Option**: Use Groq for free testing with good performance
- **Best Reasoning**: Use OpenAI GPT-4 for most sophisticated reasoning
- **Cost-Effective**: Use smaller models for simple tasks
- **Interactive Mode**: Try different queries to see ReAct reasoning in action