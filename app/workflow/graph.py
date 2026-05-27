from __future__ import annotations

from typing import Protocol

from langgraph.graph import StateGraph, END

from app.core.llm import LLMClient
from app.schemas.documents import DOCUMENT_SPECS
from app.schemas.state import MVPilotState
from app.workflow.nodes import build_document_node, idea_intake_node


class Workflow(Protocol):
    def invoke(self, state: MVPilotState) -> MVPilotState:
        """Run the workflow and return the updated state."""


def build_workflow(llm: LLMClient) -> Workflow: 
    graph = StateGraph(MVPilotState)

    graph.add_node("idea_intake", idea_intake_node)
    
    previous = "idea_intake"
    for spec in DOCUMENT_SPECS:
        graph.add_node(spec.node_name, build_document_node(spec, llm))
        graph.add_edge(previous, spec.node_name)
        previous = spec.node_name

    graph.add_edge(previous, END)
    graph.set_entry_point("idea_intake")
    
    return graph.compile()
