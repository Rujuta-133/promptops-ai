from fastapi import FastAPI, Depends
from backend.schemas.prompt import PromptCreate
from backend.database.session import get_db
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "PromptOps AI is running"}


@app.post("/prompts")
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    return prompt.model_dump()