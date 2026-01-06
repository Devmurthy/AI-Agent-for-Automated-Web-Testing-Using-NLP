# workflow.py

def generate_test_steps(actions):
    steps = []

    for act in actions:
        if act["action"] == "goto":
            steps.append(f"Open the webpage: {act['target']}")

        elif act["action"] == "type":
            steps.append(f"Type '{act['value']}' into {act['target']}")

        elif act["action"] == "click":
            steps.append(f"Click on {act['target']}")

    return steps
