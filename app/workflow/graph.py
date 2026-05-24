from __future__ import annotations

from typing import Protocol

from app.schemas.documents import DOCUMENT_SPECS
from app.schemas.state import MVPilotState
from app.workflow.nodes import build_document_node, idea_intake_node


class Workflow(Protocol):
    def invoke(self, state: MVPilotState) -> MVPilotState:
        """Run the workflow and return the updated state."""


class SequentialWorkflow:
    def __init__(self) -> None:
        self._nodes = [idea_intake_node, *[build_document_node(spec) for spec in DOCUMENT_SPECS]]

    def invoke(self, state: MVPilotState) -> MVPilotState:
        current = dict(state)
        for node in self._nodes:
            current.update(node(current))
        return current


def build_workflow() -> Workflow:
    try:
        from langgraph.graph import END, StateGraph
    except ImportError:
        return SequentialWorkflow()

    graph = StateGraph(MVPilotState)
    graph.add_node("idea_intake", idea_intake_node)
    previous = "idea_intake"

    for spec in DOCUMENT_SPECS:
        graph.add_node(spec.node_name, build_document_node(spec))
        graph.add_edge(previous, spec.node_name)
        previous = spec.node_name

    graph.add_edge(previous, END)
    graph.set_entry_point("idea_intake")
    return graph.compile()
