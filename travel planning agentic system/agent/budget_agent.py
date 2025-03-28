from agents import Agent , Runner , WebSearchTool , input_guardrail , GuardrailFunctionOutput
from dotenv import load_dotenv
import os
from models.budget_model import BudgetAnalysis
from tools.mcp_server import get_tavily_mcp_server

## Get the llm model from the environment variables
load_dotenv()
model = os.getenv("MODEL_CHOICE")

### System prompt
budget_agent_system_prompt = """
    Overview
    You are a Budget Agent. Your task is to analyze travel budgets to determine if they are realistic for the destination and duration.
    Consider factors like:
    - Average hotel costs in the destination
    - Flight costs
    - Food and entertainment expenses
    - Local transportation
    
    Execution Flow
    - Make to search through web resources to find average costs for the destination.
    - Analyze the user's budget and compare it to the estimated costs for the trip.
    - Provide recommendations if the budget is not realistic.
    
    Important Note :
    Provide a clear analysis of whether the budget is realistic and why.
    If the budget is not realistic, suggest a more appropriate budget.
    Don't be harsh at all, lean towards it being realistic unless it's really crazy.
    If no budget was mentioned, just assume it is realistic.
"""

### Budget Analysis Agent
budget_agent = Agent(
    model=model,
    name="Budget Agent",
    instructions=budget_agent_system_prompt,
    output_type=BudgetAnalysis,
)

@input_guardrail
async def budget_guardrail(ctx, agent, input_data):
    """Check if the user's travel budget is realistic."""
    # Parse the input to extract destination, duration, and budget
    try:
        analysis_prompt = f"The user is planning a trip and said: {input_data}.\nAnalyze if their budget is realistic for a trip to their destination for the length they mentioned."
        result = await Runner.run(budget_agent, analysis_prompt, context=ctx.context)
        final_output = result.final_output_as(BudgetAnalysis)

        # if not final_output.is_within_budget:
        #     print(f"Your budget for your trip may not be realistic. {final_output.recommendations}" if not final_output.is_within_budget else None)
         
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not final_output.is_within_budget,
        )
    except Exception as e:
        # Handle any errors gracefully
        return GuardrailFunctionOutput(
            output_info=BudgetAnalysis(),  
            tripwire_triggered=False
        )
