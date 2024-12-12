from workflows.states import ReflectionState
from langchain_core.messages import AIMessage
from workflows.chains import first_responder_chain

def revisor_node(state: ReflectionState):
    res = first_responder_chain.stream({
        "messages": state["messages"] 
    })
     
    return {
        "messages": [AIMessage(content=res)],
    }