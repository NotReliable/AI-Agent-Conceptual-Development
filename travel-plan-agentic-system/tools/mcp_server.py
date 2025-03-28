from agents import Agent, Runner, gen_trace_id, trace
from agents.mcp import MCPServerSse , MCPServer , MCPServerStdio 
import asyncio
import shutil
from dotenv import load_dotenv
import os

load_dotenv()

async def get_tavily_mcp_server():
    return MCPServerStdio(
        name="tavily-mcp",
        params={
            "command": "npx.cmd",
            "args": ["-y", "tavily-mcp@0.1.4"],
            "env": {
                "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
            },
        },
        cache_tools_list=True,
    )

async def main():
    mcp_server = await get_tavily_mcp_server()
    async with mcp_server as server:
        agent = Agent(
            name="Assistant",
            mcp_servers=[server],
        )
        message = "Who's elon musk networth today?"
        print("\n" + "-" * 40)
        print(f"Running: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print(result.final_output)
        
        
# async def run(mcp_server: MCPServer):
#     agent = Agent(
#         name="Assistant",
#         mcp_servers=[mcp_server],
#     )

#     message = "Who's elon musk networth today?"
#     print("\n" + "-" * 40)
#     print(f"Running: {message}")
#     result = await Runner.run(starting_agent=agent, input=message)
#     print(result.final_output)

#     message = "Summarize the last change in the repository."
#     print("\n" + "-" * 40)
#     print(f"Running: {message}")
#     result = await Runner.run(starting_agent=agent, input=message)
#     print(result.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())