import sys
import yaml
import re

def sanitize_label(text):
    return re.sub(r"[^a-zA-Z0-9_]", "_", str(text))[:40]

def get_step_id(step):
    if isinstance(step, dict) and "id" in step:
        return str(step["id"])
    return str(step)

def flatten_steps(steps):
    flat = {}
    for step in steps:
        if isinstance(step, dict):
            step_id = str(step.get("id"))
            if step_id:
                flat[step_id] = step
    return flat

def extract_transitions(step_id, branches, label):
    edges = []
    for branch in branches:
        if isinstance(branch, dict):
            if "next" in branch:
                next_steps = branch["next"]
                if isinstance(next_steps, list):
                    for target in next_steps:
                        target_id = get_step_id(target)
                        edges.append((step_id, target_id, label))
                elif isinstance(next_steps, dict):  # edge case
                    edges.append((step_id, get_step_id(next_steps), label))
            elif "capture_flag" in branch:
                edges.append((step_id, f"{step_id}_flag_{sanitize_label(branch['capture_flag'])}", "🎯"))
            elif "log" in branch:
                edges.append((step_id, f"{step_id}_log_{sanitize_label(branch['log'])}", "🪵"))
    return edges

def extract_conditions(step):
    edges = []
    sid = get_step_id(step)
    for cond in step.get("conditions", []):
        label = f"match: {cond.get('match', '')}"
        for target in cond.get("next", []):
            target_id = get_step_id(target)
            edges.append((sid, target_id, label))
    return edges

def generate_mermaid(data):
    steps = data["attack"]["steps"]
    flat_steps = flatten_steps(steps)

    lines = ["flowchart TD"]
    edges = []

    for sid, step in flat_steps.items():
        lines.append(f'    {sid}["{sid}: {step["name"]}"]')
        edges.extend(extract_transitions(sid, step.get("on_success", []), "✅"))
        edges.extend(extract_transitions(sid, step.get("on_failure", []), "❌"))
        edges.extend(extract_conditions(step))

    for src, tgt, label in edges:
        lines.append(f'    {src} -->|{label}| {tgt}')

    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python yaml_to_mermaid.py <file.yaml>")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        try:
            data = yaml.safe_load(f)
            mermaid = generate_mermaid(data)
            print(mermaid)
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
