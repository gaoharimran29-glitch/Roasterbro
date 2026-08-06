from pydantic import BaseModel, Field

class Question(BaseModel):
    question: str = Field(
        min_length=1, 
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
        min_length=1, 
        description="Final Roast based on repo data and interrogation with questions"
    )
