import warnings
import os
import subprocess
import re
import yaml
import sys

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
    if "steps" not in attack_tree or not isinstance(attack_tree["steps"], list):
        raise ValueError("❌ Error: Invalid attack tree format. 'steps' key must be a list.")

def hack(hack_name):
    print(f"Executing hack: {hack_name}")
    
    yaml_file = f"{hack_name}.yaml"
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

def execute_attack_tree(attack_tree):
    """
    Execute a structured attack tree with preconditions, variable substitution, and conditional logic.
    """
    steps = {step["id"]: step for step in attack_tree["steps"]}
    visited = set()
    variables = {}
    captured_flags = []

    def substitute_variables(text):
        for var, val in variables.items():
            text = text.replace(f"{{{{ {var} }}}}", val)
        return text

    def check_preconditions(preconds):
        for p in preconds:
            var = p.get("variable")
            match = p.get("match")
            if var not in variables or not re.search(match, variables[var]):
                return False
        return True

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

        if "preconditions" in step and not check_preconditions(step["preconditions"]):
            print("⏭ Preconditions not met. Skipping.")
            return

        command = substitute_variables(step.get("command", ""))
        print(f"🔄 Running: {command}")

        try:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            output = result.stdout.strip()
            print(f"✅ Output:\n{output}")
        except subprocess.CalledProcessError as e:
            output = e.output.strip() if e.output else e.stderr.strip()
            print(f"❌ Command failed:\n{output}")

        for extract in step.get("extract", []):
            name = extract["name"]
            pattern = extract["regex"]
            match = re.search(pattern, output)
            if match:
                value = match.group(1)
                variables[name] = value
                print(f"📥 Extracted variable '{name}' = '{value}'")

        if step.get("capture_flag", False):
            flag_match = re.search(r"flag\{.*?\}", output)
            if flag_match:
                flag = flag_match.group(0)
                captured_flags.append(flag)
                print(f"🏴 Flag found: {flag}")
            else:
                print("Unable to find a flag which should be here")

        if "next" in step:
            next_step_id = substitute_variables(step["next"])
            execute_step(next_step_id)
        elif "conditions" in step:
            for cond in step["conditions"]:
                pattern = cond.get("match")
                target_step = cond.get("next")
                if re.search(pattern, output):
                    execute_step(substitute_variables(target_step))
                    break

    root_step_id = attack_tree.get("start") or attack_tree["steps"][0]["id"]
    execute_step(root_step_id)

    print("\n🎯 Attack tree complete.")
    if captured_flags:
        print("Captured flags:")
        for f in captured_flags:
            print(f"  {f}")

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
    "list": list_hacks
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
