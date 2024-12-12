from workflows.states import SimpleQAState 
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from workflows.chains import first_responder_chain

def simple_qa_node(state: SimpleQAState):
    res: str = first_responder_chain.invoke({
        "messages": state["messages"]
    })
    
    return { "messages": [AIMessage(content=res)] }