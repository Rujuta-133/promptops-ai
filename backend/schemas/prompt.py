from pydantic import BaseModel

class PromptCreate(BaseModel):
    name: str
    description: str | None = None
    content : str
    variables : list[str] = [] 