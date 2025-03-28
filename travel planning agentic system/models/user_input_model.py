from pydantic import BaseModel, Field
from typing import List, Optional

class UserInputDetails(BaseModel):
    destination : str = Field(description="The destination city or country for the trip")
    duration : int = Field(description="The number of days for the trip")
    start_date : str = Field(description="The start date of the trip")
    end_date : str = Field(description="The end date of the trip")
    budget : Optional[float] = Field(description="The total budget allocated for the trip")
    is_all_details_provided : bool = Field(description="Indicates whether all required details are provided for planning the trip")
    reason : str = Field(description="Reason for not providing all details")
