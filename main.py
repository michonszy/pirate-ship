import warnings
import os
import subprocess
import re
import yaml
import sys
import openai
import json


warnings.filterwarnings("ignore")

art=r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠤⠴⠶⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣾⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠂⠉⡇⠀⠀⠀⢰⣿⣿⣿⣿⣧⠀⠀⢀⣄⣀⠀⠀⠀⠀⠀⠀  _____ _            ____  _           _             _     _       
⠀⠀⠀⠀⠀⠀⢠⣶⣶⣷⠀⠀⠀⠸⠟⠁⠀⡇⠀⠀⠀⠀⠀⢹⠀⠀⠀⠀⠀⠀ |_   _| |__   ___  |  _ \(_)_ __ __ _| |_ ___   ___| |__ (_)_ __  
⠀⠀⠀⠀⠀⠀⠘⠟⢹⣋⣀⡀⢀⣤⣶⣿⣿⣿⣿⣿⡿⠛⣠⣼⣿⡟⠀⠀⠀⠀   | | | '_ \ / _ \ | |_) | | '__/ _` | __/ _ \ / __| '_ \| | '_ \ 
⠀⠀⠀⠀⠀⣴⣾⣿⣿⣿⣿⢁⣾⣿⣿⣿⣿⣿⣿⡿⢁⣾⣿⣿⣿⠁⠀⠀⠀⠀   | | | | | |  __/ |  __/| | | | (_| | ||  __/ \__ \ | | | | |_) |
⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⠿⠇⠀⠀⠀⠀   |_| |_| |_|\___| |_|   |_|_|  \__,_|\__\___| |___/_| |_|_| .__/ 
⠀⠀⠀⠳⣤⣙⠟⠛⢻⠿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣇⠘⠉⠀⢸⠀⢀⣠⠀⠀⠀                                                            |_|    
⠀⠀⠀⠀⠈⠻⣷⣦⣼⠀⠀⠀⢻⣿⣿⠿⢿⡿⠿⣿⡄⠀⠀⣼⣷⣿⣿⠀⠀⠀   Kubernetes hacking tool ☸🏴‍☠️
⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⣶⣄⡈⠉⠀⠀⢸⡇⠀⠀⠉⠂⠀⣿⣿⣿⣧⠀⠀⠀     by Szymon Michoń
⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣷⣤⣀⣸⣧⣠⣤⣴⣶⣾⣿⣿⣿⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
      
"""

def get_kube_prompt():
    try:
        # Get current context
        context = subprocess.run(
            ["kubectl", "config", "current-context"],
            check=True, capture_output=True, text=True
        ).stdout.strip()

        # Get current namespace
        namespace = subprocess.run(
            ["kubectl", "config", "view", "--minify", "--output", "jsonpath={..namespace}"],
            check=True, capture_output=True, text=True
        ).stdout.strip()

        if not namespace:
            namespace = "default"

        return f"{context}:{namespace}"
    
    except subprocess.CalledProcessError:
        print("\n❌ No Kubernetes context is currently active or you are not logged into any cluster.\n")
        print("🔐 Please log into a cluster first. Here are common options:\n")
        print("👉 1. Start a local cluster using Rancher Desktop, Minikube, or Kind")
        print("👉 2. Connect to a cloud cluster:")
        print("     • AWS:      aws eks update-kubeconfig --name <cluster-name>")
        print("     • GCP:      gcloud container clusters get-credentials <cluster-name>")
        print("     • Azure:    az aks get-credentials --name <cluster-name>")
        print("👉 3. Authenticate with your provider (if using SSO/OIDC)")
        print("👉 4. Check config:  kubectl config get-contexts")
        print("👉 5. Set a context: kubectl config use-context <name>\n")
        print("💡 Once connected, re-run this tool.\n")
        sys.exit(1)
        

CLUSTER_IP = get_kube_prompt()
HACK_NAME = "example_hack"
openai.api_key = os.getenv("OPENAI_API_KEY")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def validate_attack_tree(attack_tree):
    # Try both flat and nested formats
    if "steps" in attack_tree and isinstance(attack_tree["steps"], list):
        return "flat"
    elif "attack" in attack_tree and "steps" in attack_tree["attack"] and isinstance(attack_tree["attack"]["steps"], list):
        return "nested"
    else:
        raise ValueError("❌ Error: Invalid attack tree format. No valid 'steps' list found.")

def execute_attack_tree(attack_tree):
    """
    Execute a structured attack tree with support for nested 'attack' block.
    Dynamically captures any FLAG{...} patterns found in command outputs.
    """
    format_type = validate_attack_tree(attack_tree)

    if format_type == "nested":
        attack_tree = attack_tree["attack"]

    steps = {step["id"]: step for step in attack_tree["steps"]}
    visited = set()
    variables = {var["name"]: var["value"] for var in attack_tree.get("variables", [])}
    captured_flags = []  # Stores only actually found flags

    def substitute_variables(text):
        for var, val in variables.items():
            text = text.replace(f"${{{var}}}", val)
        return text

    def execute_step(step_id):
        if step_id in visited:
            print(f"⚠️ Step {step_id} already executed. Skipping.")
            return
        visited.add(step_id)

        step = steps.get(step_id)
        if not step:
            print(f"❌ No step with ID: {step_id}")
            return

        print(f"\n➡️ Executing step: {step.get('name', step_id)}")

        command = substitute_variables(step.get("command", ""))
        print(f"🔄 Running: {command}")

        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = result.stdout.strip()
            print(f"✅ Output:\n{output}")
            # Dynamic flag capture from command output
            found_flags = re.findall(r'FLAG\{[^}]+\}', output)
            for flag in found_flags:
                if flag not in captured_flags:
                    captured_flags.append(flag)
                    print(f"🏴 Captured flag: {flag}")

            # Handle on_success actions (excluding YAML flag declarations)
            if step.get("on_success"):
                for action in step["on_success"]:
                    if isinstance(action, dict) and "remediate" in action:
                        print(f"💡 Suggested fix: {action['remediate']}")
                    elif isinstance(action, dict) and "next" in action:
                        execute_step(action["next"])

        except subprocess.TimeoutExpired:
            print(f"⏰ Command timed out after 60 seconds: {command}")
            output = f"Command timed out after 60 seconds: {command}"
            raise subprocess.CalledProcessError(1, command, output)

        except subprocess.CalledProcessError as e:
            output = e.output.strip() if e.output else e.stderr.strip()
            print(f"❌ Command failed:\n{output}")

            # Also check for flags in error output
            found_flags = re.findall(r'FLAG\{[^}]+\}', output)
            for flag in found_flags:
                if flag not in captured_flags:
                    captured_flags.append(flag)
                    print(f"🏴 Captured flag in error output: {flag}")

            # Failure handling
            if step.get("on_failure"):
                for action in step["on_failure"]:
                    if isinstance(action, dict) and "next" in action:
                        print(f"⏭️ Proceeding to next step after failure: {action['next']}")
                        execute_step(action["next"])
                    elif isinstance(action, dict) and "remediate" in action:
                        print(f"💡 Suggested fix: {action['remediate']}")
            elif step.get("next"):
                print(f"⏭️ Proceeding to next step: {step['next']}")
                execute_step(step["next"])

    root_step_id = attack_tree.get("start") or attack_tree["steps"][0]["id"]
    execute_step(root_step_id)

    print("\n🎯 Attack tree execution complete.")
    if attack_tree.name.lower().startswith("recon"):
        print("\n🧠 Recon Summary:")
        for step in executed_steps:
            if step.result and step.result.stdout:
                print(f"\n🔹 {step.name}")
                print(step.result.stdout.strip())
        print("\n🎯 Recon complete.")
    else:
        if captured_flags:
            print("\n✅ Flags captured:")
            for flag in captured_flags:
                print(f"🏁 {flag}")
        else:
            print("\n🎯 Attack tree execution complete.")
            print("No flags were captured during execution.")

def hack(hack_name):
    """
    Everything setted up? Let's execute this!
    """
    print(f"Executing hack: {hack_name}")
    
    yaml_file = f"rag/attack-trees/{hack_name}.yml"
    if not os.path.isfile(yaml_file):
        yaml_file_alt = f"{hack_name}.yml"
        if os.path.isfile(yaml_file_alt):
            yaml_file = yaml_file_alt
        else:
            print(f"❌ Error: No .yaml or .yml file found for this hack.")
            return True

    try:
        with open(yaml_file, "r") as file:
            attack_tree = yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"❌ Error: Failed to parse YAML file '{yaml_file}': {e}")
        return True

    try:
        validate_attack_tree(attack_tree)
        execute_attack_tree(attack_tree)
    except Exception as e:
        print(f"❌ Error: while executing attack: {e}")
        return True

    print(f"✅ Successfully executed hack: {hack_name}")
    return True


def list_hacks():
    """
    Lists all available hack JSON files in the specified directory
    and allows the user to select one dynamically.
    """
    global HACK_NAME
    directory = 'rag/attack-trees'
    hack_files = [f for f in os.listdir(directory) if f.endswith(".yaml") or f.endswith(".yml")]

    if not hack_files:
        print("❌ No hack files (.yaml/.yml) found in the directory.")
        return True

    print("🔍 Available Hacks:")
    for i, file in enumerate(hack_files, start=1):
        print(f"  {i}. {file}")

    while True:
        try:
            choice = input("\nEnter the number of the hack to select (or 'q' to cancel): ")
            if choice.lower() == 'q':
                print("❌ Hack selection canceled.")
                return True

            choice_index = int(choice) - 1
            if 0 <= choice_index < len(hack_files):
                HACK_NAME = os.path.splitext(hack_files[choice_index])[0]
                print(f"✅ Hack selected: {HACK_NAME}")
                return True
            else:
                print("⚠️ Invalid choice. Please select a valid number.")
        except ValueError:
            print("⚠️ Invalid input. Please enter a number or 'q'.")

def hello():
    """Greet the user."""
    print("Hello, user! How can I help you?")
    return True

def exit():
    """Exit the application."""
    print("Goodbye! Exiting the app...")
    return False

def status():
    """Show the current status."""
    print("🔍 Checking Kubernetes cluster status...\n")

    try:
        subprocess.run(
            ["kubectl", "cluster-info"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        print("✅ Connection to Kubernetes cluster is active.\n")
        return True

    except subprocess.CalledProcessError:
        print("❌ Cannot connect to a Kubernetes cluster.\n")
        print("📋 Troubleshooting steps:")
        print("  • Ensure you are logged in and have context set.")
        print("  • Check if VPN or local cluster (e.g., Rancher Desktop) is running.")
        print("  • Run: kubectl config get-contexts")
        print("  • Use: kubectl config use-context <context-name>\n")
        return True

def auto_hack():
    """Run reconnaissance and let GPT-driven AI decide next steps."""
    print("🧠 Starting automated hacking process...")

    # Step 1: Run reconnaissance
    recon_file = os.path.join('rag/attack-trees', "recon.yaml")
    if not os.path.isfile(recon_file):
        print("❌ Reconnaissance tree (recon.yaml) not found.")
        return True

    with open(recon_file, "r") as f:
        recon_tree = yaml.safe_load(f)
    
    outputs = []
    variables = {}

    def capture_output_from_tree(tree):
        nonlocal variables, outputs
        steps = {s["id"]: s for s in tree["steps"]}
        start = tree.get("start", tree["steps"][0]["id"])

        def run_step(sid):
            step = steps.get(sid)
            if not step: return
            command = step.get("command")
            if command:
                print(f"🔍 Recon: {command}")
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
                    out = result.stdout.strip()
                    outputs.append({"command": command, "output": out})
                    print(f"✅ {out}")
                    for ex in step.get("extract", []):
                        name = ex["name"]
                        match = re.search(ex["regex"], out)
                        if match:
                            variables[name] = match.group(1)
                except subprocess.CalledProcessError as e:
                    outputs.append({"command": command, "output": e.stderr.strip()})
                    print(f"❌ {e.stderr.strip()}")
            if "next" in step:
                run_step(step["next"])

        run_step(start)

    capture_output_from_tree(recon_tree)

    # Step 2: Build GPT prompt
    system_msg = {
        "role": "system",
        "content": (
            "You are an offensive Kubernetes penetration testing assistant. "
            "Based on previous reconnaissance, respond with ready-to-run kubectl/bash commands. "
            "Do not explain. Only return actual commands to run."
        )
    }

    history = [
        {"role": "user", "content": json.dumps(outputs, indent=2)}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Replace with your custom model if needed
            messages=[system_msg] + history,
            temperature=0.2
        )
        reply = response.choices[0].message["content"]
        print("\n🤖 Suggested command(s):\n", reply)

        # Step 3: Execute the commands
        for line in reply.strip().splitlines():
            if not line.strip(): continue
            print(f"\n⚔️ Running: {line}")
            try:
                res = subprocess.run(line, shell=True, check=True, capture_output=True, text=True)
                out = res.stdout.strip()
                print(f"✅ Output:\n{out}")
                # Optionally: feed this back for another GPT step
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed:\n{e.stderr.strip()}")

    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
    
    return True


def setup():
    """Setup tool"""
    print("Current setup")
    print(f"Victim ip: {CLUSTER_IP}")
    print(f"Hack name: {HACK_NAME}")
    print("Mode: recognition")
    print("Attak type: AI")
    chg = input("Do you want to change it? [Y/N] : ")
    if chg.lower() == 'y':
        print("Change mode")
    else:
        print("No changes were made")
    return True

def help():
    print("\nAvailable commands:")
    for command in COMMANDS:
        print(f"{command} - {COMMANDS[command].__doc__}")
    print()
    return True

COMMANDS = {
    "hello": hello,
    "exit": exit,
    "status": status,
    "help": help,
    "setup": setup,
    "hack": lambda: hack(HACK_NAME),
    "list": list_hacks,
    "auto": auto_hack

}

def handle_command(command):
    command_func = COMMANDS.get(command.lower())
    if command_func:
        return command_func() 
    else:
        print(f"Unknown command")
        return True
    
def main():
    print(art) 
    running = True
    while running:
        command = input(f"╭─ "+bcolors.WARNING+CLUSTER_IP+ bcolors.ENDC+" > "+bcolors.FAIL+HACK_NAME+ bcolors.ENDC+" \n╰─➤ ")
        running = handle_command(command)

if __name__ == "__main__":
    main()
