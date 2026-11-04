from fastapi import FastAPI
from backend.schemas.prompt import PromptCreate

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "PromptOps AI is running"}


@app.post("/prompts")
def create_prompt(prompt: PromptCreate):
    return prompt.model_dump()