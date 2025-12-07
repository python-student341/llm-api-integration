from pydantic import Field, BaseModel

class GetAIAnswerShema(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)