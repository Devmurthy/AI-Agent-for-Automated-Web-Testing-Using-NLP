# workflow.py

def generate_test_steps(actions):
    steps = []

    for act in actions:
        action = act.get("action")

        if action == "goto":
            steps.append("Open the login page")

        elif action == "fill":
            value = act.get("value", "")
            steps.append(f'Enter "{value}" into the username field')

        elif action == "click":
            steps.append("Click on the login button")

    return steps

