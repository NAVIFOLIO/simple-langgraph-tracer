"""
This module provides settings of LangGraph which is executed by Streamlit frontend.

1. Import your Graph builder (not compiled) here and assign it to YOUR_GRAPH_BUILDER statement.
2. Modify YOUR_CUSTOM_INPUT argument so that graph input matches to your Graph's custom states.

example:
    Let's say you did build smart researcher AI who answers questions within a specified word count.

        class ResearcherAgentState(MessagesState):
            user_question: str
            word_count: int
            answer: str 
            critique: str
            searched_queries: List[str]

    - Custom Inputs
        1. You added "user_question" to initial input, so that nodes in later part of your process can fetch user query from graph state.
        2. You added "word_count" to initial input for the same reason.
    
    YOUR_CUSTOM_INPUT should be:
        
        YOUR_CUSTOM_INPUT: Dict = {
            "user_question": prompt,
            "word_count": 250
        }

As noted in the following langgraph guide, It is reccomended that your custom state of graph inherit MessagesState Class, so I asssume you design so.
But if you wouldn't do that, you must also modify [1] app.py file (streamlit frontend), [2] utils/boot_graph.py file not to call graph with "messages" argument.   

- Working with Messages in Graph State: "https://langchain-ai.github.io/langgraph/concepts/low_level/#working-with-messages-in-graph-state"
     
Copyright (c) 2024 NAVIFOLIO
Licensed under the Apache 2.0 License
"""

from typing import Dict, List, Tuple, TypedDict
from langgraph.graph import Graph
from utils import boot_graph
# Graph samples.
from workflows import (
    simple_qa_graph_builder,
    reflect_graph_builder
)
from workflows.states import SimpleQAState, ReflectionState

# Change this to your graph builder.
YOUR_GRAPH_BUILDER: Graph = simple_qa_graph_builder
# Change this to graph state class.
YOUR_GRAPH_STATE: Dict = SimpleQAState 

def BOOT_GRAPH(prompt: str, history: List[Tuple[str, str]]):

    # Change this to your custom input.
    YOUR_CUSTOM_INPUT: Dict = {
       "query": prompt
    }

    return boot_graph(
        input = YOUR_CUSTOM_INPUT,
        prompt=prompt,
        history=history,
        graph_builder=YOUR_GRAPH_BUILDER
    )

# Don't change this.
MERMAID = YOUR_GRAPH_BUILDER.compile().get_graph().draw_mermaid()