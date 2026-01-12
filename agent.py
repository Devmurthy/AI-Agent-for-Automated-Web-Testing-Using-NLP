# # agent.py
# from langgraph.graph import StateGraph, START, END
# from transformers import pipeline

# # --- Load Local Model (NO API KEY REQUIRED) ---
# # This loads distilgpt2 model inside the venv
# model = pipeline("text-generation", model="distilgpt2")

# def local_llm_node(state: dict):
#     text = state.get("input", "")

#     # Generate response locally
#     out = model(
#         text,
#         max_length=50,
#         num_return_sequences=1,
#         pad_token_id=50256  # needed to avoid warnings
#     )

#     reply = out[0]['generated_text']
#     return {"response": reply}

# # --- Build Graph ---
# def build_agent():
#     g = StateGraph(dict)
#     g.add_node("agent", local_llm_node)
#     g.add_edge(START, "agent")
#     g.add_conditional_edges("agent", lambda s: END, [END])
#     return g.compile()

# AGENT = build_agent()

# # Main entry used by Flask
# def handle_input(user_text: str):
#     state = {"input": user_text}
#     final_state = AGENT.invoke(state)
#     return final_state.get("response", "")




# agent.py

from langgraph.graph import StateGraph, START, END
from instruction_parser import parse_instruction
from workflow import generate_test_steps

# -----------------------------
# Node 1: Parse user input
# -----------------------------
def parser_node(state):
    user_input = state.get("input", "")
    parsed_actions = parse_instruction(user_input)
    return {
        **state,
        "parsed_actions": parsed_actions
    }

# -----------------------------
# Node 2: Generate test steps
# -----------------------------
def generator_node(state):
    actions = state.get("parsed_actions", [])
    steps = generate_test_steps(actions)
    return {
        **state,
        "generated_steps": steps
    }

# -----------------------------
# Node 3: Execute test (Demo level)
# -----------------------------
def execution_node(state):
    # Future lo ikkada Playwright execution add cheyyachu
    execution_result = "Test executed successfully in headless mode"
    return {
        **state,
        "execution_status": execution_result
    }

# -----------------------------
# Node 4: Reporting
# -----------------------------
def report_node(state):
    return {
        "parsed_actions": state.get("parsed_actions", []),
        "generated_steps": state.get("generated_steps", []),
        "execution_status": state.get("execution_status", "")
    }

# -----------------------------
# Build LangGraph workflow
# -----------------------------
def build_agent():
    g = StateGraph(dict)

    g.add_node("parser", parser_node)
    g.add_node("generator", generator_node)
    g.add_node("executor", execution_node)
    g.add_node("report", report_node)

    g.add_edge(START, "parser")
    g.add_edge("parser", "generator")
    g.add_edge("generator", "executor")
    g.add_edge("executor", "report")
    g.add_edge("report", END)

    return g.compile()

# Compile agent
AGENT = build_agent()

# -----------------------------
# Flask entry function
# -----------------------------
def handle_input(user_text: str):
    state = {"input": user_text}
    final_state = AGENT.invoke(state)
    return final_state
