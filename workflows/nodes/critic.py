from workflows.states import ReflectionState
from workflows.schemas import Critique
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from workflows.chains import critic_chain

def critic_node(state: ReflectionState):
    res: Critique = critic_chain.invoke({
        "messages": state["messages"],
        "query": state["query"],
        "answer": state["first_answer"]
    })
    
    res_dict = res.to_dict()

    template=f"""
Revise [first answer] to [user question] based on the critique.
The critique to [first answer] is given below at 2 points [missing] and [superfluous].
    
user question: {state["query"]}
first answer: {state["first_answer"]}
missing: {res_dict["missing"]}
superfluous: {res_dict["superfluous"]}

YOUR RESPONSE:
"""

    return {
        "messages": HumanMessage(content=template),
        "missing": res_dict["missing"],
        "superfluous": res_dict["superfluous"]
    }