import copy
import sqlite3
import uuid
import os
from typing import List, Tuple, Dict, Any
from langgraph.graph import Graph
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage

def boot_graph(input: Dict, prompt: str, history: List[Tuple[str, str]], graph_builder: Graph) -> Tuple[str, Any]:
    conn = sqlite3.connect(
        database=os.environ["DATABASE_PATH"],
        check_same_thread=False
    )
    memory = SqliteSaver(conn)

    graph = graph_builder.compile(
        checkpointer=memory,
    )
    thread = {
        "configurable": { "thread_id": str(uuid.uuid4()) }
    }
    
    messages = copy.deepcopy(history)
    messages.append(HumanMessage(content=prompt))
    input["messages"] = messages

    initial_input = input 
    
    return (
        thread["configurable"]["thread_id"],
        graph.stream(
            input=initial_input,
            config=thread,
            stream_mode=["values"]
        )
    )