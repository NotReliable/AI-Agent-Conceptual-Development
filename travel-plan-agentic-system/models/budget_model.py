from pydantic import BaseModel, Field
from typing import List, Optional

class BudgetAnalysis(BaseModel):
    total_estimated_cost: Optional[float] = Field(default=None, description="Total estimated cost for the entire travel plan")
    transport_cost: Optional[float] = Field(default=None, description="Estimated cost for all transportation (flights, local transport, transfers)")
    accommodation_cost: Optional[float] = Field(default=None, description="Estimated cost for accommodation throughout the trip")
    dining_cost: Optional[float] = Field(default=None, description="Estimated cost for meals and dining experiences")
    activities_cost: Optional[float] = Field(default=None, description="Estimated cost for sightseeing, tours, and other activities")
    misc_cost: Optional[float] = Field(default=None, description="Estimated cost for miscellaneous expenses (shopping, extras, etc.)")
    is_within_budget: bool = Field(description="Indicates whether the total estimated cost is within the user's budget")
    recommendations: Optional[str] = Field(default=None, description="Advice or adjustments to help the user align the plan with their budget")
