import sys
import yaml
import re

def extract_variables_from_string(s):
    return re.findall(r"\${([a-zA-Z_][a-zA-Z0-9_]*)}", s)

def collect_all_strings(data):
    if isinstance(data, dict):
        for v in data.values():
            yield from collect_all_strings(v)
    elif isinstance(data, list):
        for v in data:
            yield from collect_all_strings(v)
    elif isinstance(data, str):
        yield data

def validate_attack_tree(data):
    errors = []

    if "attack" not in data:
        errors.append("Missing top-level 'attack' key.")
        return errors

    attack = data["attack"]

    declared_vars = set()
    if "variables" in attack:
        for var in attack["variables"]:
            if "name" in var:
                declared_vars.add(var["name"])

    steps = attack.get("steps", [])
    for idx, step in enumerate(steps):
        for string in collect_all_strings(step):
            used_vars = extract_variables_from_string(string)
            for var in used_vars:
                if var not in declared_vars:
                    errors.append(f"Variable '${{{var}}}' used before declaration at attack.steps[{idx}]")

    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python format_validator.py <file.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        with open(filepath, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"❌ YAML parsing error: {e}")
        sys.exit(1)

    issues = validate_attack_tree(data)
    if issues:
        print("❌ Validation failed with the following issues:")
        for issue in issues:
            print(f" - {issue}")
        sys.exit(1)
    else:
        print("✅ Format is valid.")
