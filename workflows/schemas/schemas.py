from pydantic import BaseModel, Field
from typing import Any, Dict, List
from langchain_core.output_parsers import PydanticOutputParser

class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")

class Critique(BaseModel):
    """Answer the question."""
    first_answer: str = Field(description="first generated answer to the user's question.")
    reflection: Reflection = Field(description="Your reflection on the intial answer.")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "first_answer": self.first_answer,
            "missing": self.reflection.missing,
            "superfluous": self.reflection.superfluous
        }

critique_parser = PydanticOutputParser(pydantic_object=Critique)