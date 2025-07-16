import os
import asyncio
from dotenv import load_dotenv
import wikipedia
from datetime import datetime
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory


# ---------------------
# Step 1: Load Environment Variables
# ---------------------
load_dotenv()
openai_api_key = os.getenv("subscription_key")
deployment = os.getenv("deployment")
endpoint = os.getenv("endpoint")
api_version = os.getenv("api_version")


# ---------------------
# Step 2: Define Tools
# ---------------------
def get_current_datetime(*args, **kwargs):
    return datetime.now().isoformat()

def get_wikipedia_summary(query):
    try:
        return wikipedia.summary(query)
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation error: {e}"
    except wikipedia.exceptions.PageError:
        return "Page not found."
    except Exception as e:
        return str(e)


# List of tools
tools = [
    Tool(
        name="Date Time",
        func=get_current_datetime,
        description="Useful for checking the current date and time."
    ),
    Tool(
        name="Wikipedia",
        func=get_wikipedia_summary,
        description="Useful for getting Wikipedia summaries."
    ),
]


# ---------------------
# Step 3: Load Prompt and LLM
# ---------------------
prompt = hub.pull("hwchase17/react")

llm = AzureChatOpenAI(
    azure_deployment=deployment,
    azure_endpoint=endpoint,
    api_key=openai_api_key,
    api_version=api_version,
    temperature=0,
)


# ---------------------
# Step 4: Set Up Memory (summary + last messages)
# ---------------------
memory = ConversationSummaryBufferMemory(
    llm=llm,
    memory_key="chat_history",
    max_token_limit=150,           # how large the summary should be
    return_messages=True,          # required for agents
    k=10                           # keep last 10 interactions (5 user + 5 assistant)
)

# ---------------------
# Step 5: Build Agent and Executor
# ---------------------
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
    stop_sequence=True
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
)


# ---------------------
# Step 6: Async Main Loop
# ---------------------
async def main():
    print("🤖 ReAct Agent with Tools and Memory (LangChain + Azure OpenAI)")
    while True:
        query = input("\nAsk something (or 'quit'): ")
        if query.lower() == "quit":
            break
        response = await agent_executor.ainvoke({"input": query})
        print("\n📣 Response:\n", response["output"])


if __name__ == '__main__':
    asyncio.run(main())