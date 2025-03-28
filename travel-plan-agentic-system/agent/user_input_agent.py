from agents import Agent , Runner , WebSearchTool , input_guardrail , GuardrailFunctionOutput
from dotenv import load_dotenv
import os
from models.user_input_model import UserInputDetails

## Get the llm model from the environment variables
load_dotenv()
model = os.getenv("MODEL_CHOICE")


### System prompt
system_prompt = """
    # Overview:
    You are the User Input Processing Agent. Your responsibility is to ensure that the user has provided all the necessary details for planning their trip. 
    You validate, structure, and enhance the user's input before passing it to the Travel Planning Orchestrator.

    # Required User Input:
    Before proceeding, ensure that the user provides the following:
    - **Destination** (City/Country)
    - **Duration of the trip** (Number of days)
    - **Start date & end date**
    - **Budget** (Optional but recommended)
    - **Travel preferences** (Optional, but useful for personalization)

    If any of these are missing, prompt the user to provide the missing details.

    # Responsibilities:
    1. **Input Validation**  
    - Check if all required fields are provided.  
    - If any details are missing, request the missing information.  

    2. **Input Structuring**  
    - Standardize date formats (YYYY-MM-DD).  
    - Ensure duration is correctly calculated if start & end dates are provided.  
    - Convert budget to a consistent format (e.g., numeric with currency).  

    3. **Enhancement & Refinement**  
    - Extract additional details if provided (e.g., travel style, activities).  
    - Identify potential inconsistencies (e.g., end date before start date).  

    4. **Provide Structured Output**  
    - Return a clean, well-structured JSON object containing all validated details.  

    # Important Notes:
    - Do **not** proceed unless all required details are complete.
    - If the user is unsure about certain details, guide them with example responses.
    - Ensure **clarity and user-friendliness** in all interactions.

    Once validation is complete, return the structured user input to the Travel Planning Orchestrator for further processing.
"""

### Budget Analysis Agent
user_input_agent = Agent(
    model=model,
    name="Budget Agent",
    instructions=system_prompt,
    output_type=UserInputDetails,
)

@input_guardrail
async def user_input_guardrail(ctx, agent, input_data):
    """Check if the details that user given sufficient to create a detailed comprehensive travel plan."""
    # Parse the input to extract destination, duration, and budget
    try:
        analysis_prompt = f"The user is planning a trip and said: {input_data}.\nAnalyze their input to ensure all necessary details are provided for planning the trip."
        result = await Runner.run(user_input_agent, analysis_prompt, context=ctx.context)
        final_output = result.final_output_as(UserInputDetails)

        if not final_output.is_all_details_provided:
            print(f"You didn't provide enough details to create a detailed comprehensive travel plan." if not final_output.is_all_details_provided else None)
         
        return GuardrailFunctionOutput(
            output_info=final_output,
            tripwire_triggered=not final_output.is_all_details_provided,
        )
    except Exception as e:
        # Handle any errors gracefully
        return GuardrailFunctionOutput(
            output_info="Test failed",
            tripwire_triggered=False
        )
