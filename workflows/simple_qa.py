from langgraph.graph import END, StateGraph ,MessageGraph
from workflows.states import SimpleQAState
from workflows.nodes import simple_qa_node

SIMPLE_QA = "simple_qa"

simple_qa_graph_builder = StateGraph(SimpleQAState)
simple_qa_graph_builder.add_node(SIMPLE_QA, simple_qa_node)

simple_qa_graph_builder.set_entry_point(SIMPLE_QA)
simple_qa_graph_builder.add_edge(SIMPLE_QA, END)

simple_qa_graph = simple_qa_graph_builder.compile()

if __name__ == "__main__":
    print(simple_qa_graph.get_graph().draw_mermaid())