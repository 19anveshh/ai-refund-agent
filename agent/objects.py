from pydantic import BaseModel,Field


class Answer(BaseModel):
    answer:str = Field(description="the answer is needed for the user question ")
    conversation: bool = Field(
    description=(
        "This is an indicator to know if the conversation should still continue or no. "
        "If the agent has made the decision about the refund this should be false. "
        "If the conversation still needs more talk then it should be True."
    ),
    default=True,
    )
class PurchaseItem(BaseModel):
    name:str = Field(description="name of the item")
    