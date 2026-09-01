"""Wire the nodes. Edges are decided by Python only."""

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from outline import nodes
from outline.state import State


def build_graph(llm, settings, checkpointer=None):
    g = StateGraph(State)
    g.add_node("ingest", nodes.ingest)
    g.add_node("annotate", nodes.annotate)
    g.add_node("plan_parts", nodes.plan_parts)
    g.add_node("plan_chapters", nodes.plan_chapters)
    g.add_node("pack_and_merge", nodes.pack_and_merge)
    g.add_node("titles", nodes.titles)
    g.add_node("assemble", nodes.assemble)
    g.add_node("validate", nodes.validate)

    g.add_edge(START, "ingest")
    g.add_conditional_edges("ingest", nodes.fan_out_annotate, ["annotate"])
    g.add_edge("annotate", "plan_parts")
    g.add_conditional_edges("plan_parts", nodes.fan_out_chapters, ["plan_chapters"])
    g.add_edge("plan_chapters", "pack_and_merge")
    g.add_conditional_edges("pack_and_merge", nodes.fan_out_titles, ["titles"])
    g.add_edge("titles", "assemble")
    g.add_edge("assemble", "validate")
    g.add_edge("validate", END)
    return g.compile(checkpointer=checkpointer or MemorySaver())
