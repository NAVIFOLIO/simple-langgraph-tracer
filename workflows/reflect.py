from langgraph.graph import END, StateGraph
from workflows.states import ReflectionState
from workflows.nodes import generation_node, critic_node, revisor_node

GENERATE = "generate"
CRITIQUE = "critique"
REVISOR = "revisor"

reflect_graph_builder = StateGraph(ReflectionState)
reflect_graph_builder.add_node(GENERATE, generation_node)
reflect_graph_builder.add_node(CRITIQUE, critic_node)
reflect_graph_builder.add_node(REVISOR, revisor_node)

reflect_graph_builder.add_edge(GENERATE, CRITIQUE)
reflect_graph_builder.add_edge(CRITIQUE, REVISOR)

reflect_graph_builder.set_entry_point(GENERATE)
reflect_graph_builder.add_edge(REVISOR, END)

reflect_graph = reflect_graph_builder.compile()

if __name__ == "__main__":
    print(reflect_graph.get_graph().draw_mermaid())