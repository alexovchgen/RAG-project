"""Консольный запуск агента без HTTP-сервиса.

python -m app.agent.runner "What is Ridge regression?"
"""
import sys

from langchain_core.messages import HumanMessage

from app.agent.graph import build_agent_graph


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print('Usage: python -m app.agent.runner "your question"', file=sys.stderr)
        raise SystemExit(2)

    graph = build_agent_graph()
    result = graph.invoke(
        {"messages": [HumanMessage(content=question)], "iteration_count": 0},
    )
    print(result["messages"][-1].content)
    print(f"iteration_count: {result['iteration_count']}")


if __name__ == "__main__":
    main()
