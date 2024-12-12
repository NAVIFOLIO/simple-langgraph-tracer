import operator
from typing import Annotated, TypedDict, List
from langgraph.graph import MessagesState

class SimpleQAState(MessagesState):
    query: str

class ReflectionState(MessagesState):
    query: str
    first_answer: str
    missing: str
    superfluous: str