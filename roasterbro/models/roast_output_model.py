from pydantic import BaseModel, Field
from typing import List


class RepoFacts(BaseModel):
    facts: List[str] = Field(
        min_length=5,
        max_length=8,
        description="List of embarrassing/funny repo facts, 5-8 items"
    )


class Question(BaseModel):
    question: str = Field(
        description="A highly engaging, controversial, brutal or polarizing 'ragebait' question."
    )
    options: list[str] = Field(
        min_length=3, 
        max_length=3, 
        description="A list of 3 provocative, ragebaiting, brutal or contrasting options for the question."
    )


class RagebaitResponse(BaseModel):
    questions: list[Question] = Field(
        min_length=3, 
        max_length=3, 
        description="A collection of exactly 3 distinct ragebait questions generated from the text."
    )


class FinalRoast(BaseModel):
    roast: str = Field(
        description="Final Roast based on repo data and interrogation with questions"
    )
    mic_drop_line: str = Field(
        description="One unforgettable closing line for the final roast"
    )
