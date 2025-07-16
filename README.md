# ReAct Agent with Tools and Memory

This Python application implements a ReAct (Reasoning and Acting) agent using LangChain and Azure OpenAI. The agent can reason through problems, use tools to gather information, and maintain conversation memory across interactions.

## Overview

The ReAct agent follows a structured approach to problem-solving:
- **Reasoning**: The agent thinks through the problem step by step
- **Acting**: It uses available tools to gather information or perform actions
- **Observing**: It analyzes the results and decides on next steps

This implementation includes:
- Tool integration (Wikipedia search, current date/time)
- Conversation memory with summarization
- Asynchronous processing for better performance
- Error handling and parsing recovery

## Features

- 🧠 **ReAct Pattern**: Implements reasoning and acting in iterative cycles
- 🛠️ **Tool Integration**: Wikipedia search and datetime tools
- 💾 **Smart Memory**: Hybrid memory system (summary + recent messages)
- ⚡ **Async Processing**: Non-blocking execution for better responsiveness
- 🔄 **Error Recovery**: Handles parsing errors and tool failures gracefully
- 🎯 **Interactive Chat**: Continuous conversation loop with the agent

## Prerequisites

- Python 3.8 or higher
- Azure OpenAI service instance with a deployed chat model
- Internet connection for Wikipedia tool
- Valid Azure OpenAI credentials

## Required Dependencies

```bash
pip install langchain langchain-openai python-dotenv wikipedia
```

## Environment Setup

Create a `.env` file in the same directory as the script:

```env
# Azure OpenAI Configuration
subscription_key=your-azure-openai-api-key
deployment=your-deployment-name
endpoint=https://your-resource-name.openai.azure.com/
api_version=2023-12-01-preview
```

## Usage

### Running the Application

1. Ensure all environment variables are properly configured
2. Install the required dependencies
3. Run the application:

```bash
python ReAct.py
```

### Interacting with the Agent

The agent will prompt you to ask questions. You can:
- Ask factual questions (it will use Wikipedia)
- Ask for current date/time
- Ask complex questions requiring reasoning
- Type 'quit' to exit

### Example Interactions

```bash
🤖 ReAct Agent with Tools and Memory (LangChain + Azure OpenAI)

Ask something (or 'quit'): What's the current date and who was Albert Einstein?

[Agent will reason through this, use the datetime tool, then search Wikipedia for Einstein]

Ask something (or 'quit'): When did he win the Nobel Prize?

[Agent remembers the previous context about Einstein and provides the answer]
```

## Architecture

### Tools Available

1. **Date Time Tool**
   - Function: `get_current_datetime()`
   - Purpose: Returns current date and time in ISO format
   - Use case: When users ask about current time/date

2. **Wikipedia Tool**
   - Function: `get_wikipedia_summary(query)`
   - Purpose: Retrieves Wikipedia article summaries
   - Error handling: Manages disambiguation and page not found errors
   - Use case: Factual information lookup

### Memory System

The application uses `ConversationSummaryBufferMemory` which provides:

- **Buffer Memory**: Keeps the last 10 interactions (5 user + 5 assistant messages)
- **Summary Memory**: Summarizes older conversations into 150 tokens
- **Hybrid Approach**: Maintains both detailed recent context and condensed historical context

### ReAct Pattern Implementation

The agent follows this cycle:
1. **Thought**: Analyzes the question and plans approach
2. **Action**: Chooses and executes appropriate tool
3. **Observation**: Reviews tool output
4. **Repeat**: Continues until question is fully answered

## Configuration Options

You can modify these parameters in the code:

```python
# Memory configuration
max_token_limit=150,           # Summary size (adjust for longer/shorter summaries)
k=10                          # Number of recent messages to keep

# LLM configuration
temperature=0,                # Deterministic responses (0) vs creative (higher values)

# Agent configuration
verbose=True,                 # Shows reasoning steps (set False for quiet mode)
handle_parsing_errors=True,   # Automatic error recovery
```

## Error Handling

The application includes comprehensive error handling:

1. **Wikipedia Tool Errors**:
   - Disambiguation errors (multiple possible pages)
   - Page not found errors
   - Network/API errors

2. **Agent Parsing Errors**:
   - Malformed responses automatically recovered
   - Continues operation without crashing

3. **Environment Errors**:
   - Missing environment variables
   - Invalid API credentials

## Customization

### Adding New Tools

To add custom tools, follow this pattern:

```python
def your_custom_function(query):
    # Your implementation here
    return "result"

# Add to tools list
tools.append(
    Tool(
        name="Your Tool Name",
        func=your_custom_function,
        description="Description of what this tool does."
    )
)
```

### Modifying Memory Behavior

Adjust memory settings based on your needs:

```python
# For longer conversations
memory = ConversationSummaryBufferMemory(
    max_token_limit=300,  # Larger summaries
    k=20                  # More recent messages
)

# For shorter, focused conversations
memory = ConversationSummaryBufferMemory(
    max_token_limit=75,   # Smaller summaries
    k=5                   # Fewer recent messages
)
```

## Troubleshooting

### Common Issues

1. **Agent Not Using Tools**
   - Check tool descriptions are clear and specific
   - Verify the prompt template is loaded correctly
   - Ensure tools are properly registered

2. **Memory Issues**
   - Reduce `max_token_limit` if responses are too long
   - Adjust `k` value for more/fewer recent messages
   - Check if `return_messages=True` is set

3. **Wikipedia Tool Failures**
   - Check internet connectivity
   - Verify Wikipedia package is installed
   - Handle disambiguation by being more specific

4. **Azure OpenAI Connection Issues**
   - Verify all environment variables are set correctly
   - Check API key validity and deployment name
   - Ensure endpoint URL is correct

### Debug Mode

Enable verbose output to see the agent's reasoning:

```python
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,  # Shows step-by-step reasoning
    handle_parsing_errors=True,
)
```

## Performance Considerations

- **Async Processing**: Uses `asyncio` for non-blocking execution
- **Memory Management**: Automatic conversation summarization prevents token limit issues
- **Tool Caching**: Consider implementing caching for frequently accessed Wikipedia pages
- **Rate Limiting**: Be mindful of Azure OpenAI rate limits for high-volume usage

## Sample Output

```
🤖 ReAct Agent with Tools and Memory (LangChain + Azure OpenAI)

Ask something (or 'quit'): What's today's date and tell me about Python programming?

> Entering new AgentExecutor chain...
I need to get today's date and information about Python programming.

Action: Date Time
Action Input: 

Observation: 2025-07-16T10:30:45.123456
Thought: Now I have today's date. Let me get information about Python programming.

Action: Wikipedia
Action Input: Python programming language

Observation: Python is a high-level, general-purpose programming language...

Thought: I now have both pieces of information requested.

Final Answer: Today's date is July 16, 2025. Python is a high-level, general-purpose programming language...

📣 Response:
Today's date is July 16, 2025. Python is a high-level, general-purpose programming language...
```

## File Structure

```
.
├── ReAct.py           # Main application file
├── ReAct_README.md    # This documentation
└── .env              # Environment variables (create this file)
```

## Dependencies Details

- **langchain**: Core framework for building LLM applications
- **langchain-openai**: Azure OpenAI integration
- **python-dotenv**: Environment variable management
- **wikipedia**: Wikipedia API access

## Next Steps

Consider enhancing the application with:
- Additional tools (web search, calculator, file operations)
- Custom prompt templates for specific use cases
- Web interface using Streamlit or Flask
- Conversation export/import functionality
- Multi-user support with session management
- Integration with other APIs (weather, news, etc.)

## Support

For issues related to:
- **LangChain**: Check the [LangChain documentation](https://python.langchain.com/)
- **Azure OpenAI**: See the [Azure OpenAI documentation](https://docs.microsoft.com/azure/cognitive-services/openai/)
- **ReAct Pattern**: Refer to the [original ReAct paper](https://arxiv.org/abs/2210.03629)

## License

This project is provided as-is for educational and demonstration purposes.
