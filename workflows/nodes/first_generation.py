from workflows.states import ReflectionState
from langchain_core.messages import HumanMessage, AIMessage
from workflows.chains import first_responder_chain

def generation_node(state: ReflectionState):
    messages = state["messages"]
    res: str = first_responder_chain.invoke({
        "messages": messages
    })
     
    return {
        "messages": [AIMessage(content=res)],
        "first_answer": res,
    }